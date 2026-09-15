import Foundation
import Vision
import CoreVideo

// EP007 isolated preprocessing. Outputs masks only; original RGB remains in source.
// Usage: PersonMatte input.mp4 output.mkv frameCount metrics.json
// The source has a 608 x 1080 portrait centered at x=656 on its 1920 x 1080 canvas.
let args = CommandLine.arguments
guard args.count == 5, let limit = Int(args[3]), limit > 0 else {
    fputs("Usage: PersonMatte input.mp4 output.mkv frameCount metrics.json\n", stderr)
    exit(2)
}
let width = 608, height = 1080, fps = 25
let frameBytes = width * height * 4
let started = Date()

func process(_ arguments: [String], input: Pipe? = nil, output: Pipe? = nil) throws -> Process {
    let task = Process()
    task.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/ffmpeg")
    task.arguments = arguments
    if let input { task.standardInput = input }
    if let output { task.standardOutput = output }
    task.standardError = FileHandle.standardError
    try task.run()
    return task
}

func readExact(_ handle: FileHandle, count: Int) throws -> Data {
    var result = Data()
    result.reserveCapacity(count)
    while result.count < count {
        guard let chunk = try handle.read(upToCount: count-result.count), !chunk.isEmpty else { break }
        result.append(chunk)
    }
    return result
}

do {
    let decoded = Pipe(), encoded = Pipe()
    let decoder = try process(["-v","error","-nostdin","-i",args[1],"-an","-frames:v",String(limit),
        "-vf","crop=608:1080:656:0","-pix_fmt","bgra","-f","rawvideo","pipe:1"], output: decoded)
    let encoder = try process(["-v","error","-nostdin","-n","-f","rawvideo","-pixel_format","gray",
        "-video_size","608x1080","-framerate","25","-i","pipe:0","-an","-c:v","ffv1",
        "-level","3","-g","1","-pix_fmt","gray","-color_range","pc",args[2]], input: encoded)
    let request = VNGeneratePersonSegmentationRequest()
    request.qualityLevel = .accurate
    request.outputPixelFormat = kCVPixelFormatType_OneComponent8
    let sequence = VNSequenceRequestHandler()
    var count = 0
    var nativeSizes = Set<String>()
    var timestamps: [Double] = []
    while count < limit {
        let data = try readExact(decoded.fileHandleForReading, count: frameBytes)
        if data.isEmpty { break }
        guard data.count == frameBytes else { throw NSError(domain:"PersonMatte", code:1, userInfo:[NSLocalizedDescriptionKey:"Incomplete decoded frame"]) }
        try autoreleasepool {
            var pixelBuffer: CVPixelBuffer?
            let attrs: [CFString:Any] = [kCVPixelBufferIOSurfacePropertiesKey: [:]]
            let status = CVPixelBufferCreate(kCFAllocatorDefault, width, height, kCVPixelFormatType_32BGRA, attrs as CFDictionary, &pixelBuffer)
            guard status == kCVReturnSuccess, let pixelBuffer else { throw NSError(domain:"PersonMatte", code:2) }
            CVPixelBufferLockBaseAddress(pixelBuffer, [])
            let stride = CVPixelBufferGetBytesPerRow(pixelBuffer)
            let base = CVPixelBufferGetBaseAddress(pixelBuffer)!
            data.withUnsafeBytes { source in
                for row in 0..<height { memcpy(base.advanced(by:row*stride), source.baseAddress!.advanced(by:row*width*4), width*4) }
            }
            CVPixelBufferUnlockBaseAddress(pixelBuffer, [])
            try sequence.perform([request], on:pixelBuffer, orientation:.up)
            guard let mask = request.results?.first?.pixelBuffer else { throw NSError(domain:"PersonMatte", code:3, userInfo:[NSLocalizedDescriptionKey:"No segmentation mask"]) }
            let mw=CVPixelBufferGetWidth(mask), mh=CVPixelBufferGetHeight(mask)
            nativeSizes.insert("\(mw)x\(mh)")
            CVPixelBufferLockBaseAddress(mask, .readOnly)
            defer { CVPixelBufferUnlockBaseAddress(mask, .readOnly) }
            let rowBytes = CVPixelBufferGetBytesPerRow(mask)
            let source = CVPixelBufferGetBaseAddress(mask)!.assumingMemoryBound(to:UInt8.self)
            var output = Data(count:width*height)
            output.withUnsafeMutableBytes { bytes in
                let dest = bytes.baseAddress!.assumingMemoryBound(to:UInt8.self)
                // Center-aligned bilinear scale in mask space, with no RGB color treatment.
                for y in 0..<height {
                    let sy = max(0,min(Double(mh-1),(Double(y)+0.5)*Double(mh)/Double(height)-0.5))
                    let y0=Int(sy), y1=min(y0+1,mh-1), fy=sy-Double(y0)
                    for x in 0..<width {
                        let sx=max(0,min(Double(mw-1),(Double(x)+0.5)*Double(mw)/Double(width)-0.5))
                        let x0=Int(sx), x1=min(x0+1,mw-1), fx=sx-Double(x0)
                        let a=Double(source[y0*rowBytes+x0])*(1-fx)+Double(source[y0*rowBytes+x1])*fx
                        let b=Double(source[y1*rowBytes+x0])*(1-fx)+Double(source[y1*rowBytes+x1])*fx
                        dest[y*width+x]=UInt8((a*(1-fy)+b*fy).rounded())
                    }
                }
            }
            try encoded.fileHandleForWriting.write(contentsOf:output)
        }
        count += 1
        if count == 1 || count % 25 == 0 {
            let elapsed=Date().timeIntervalSince(started)
            timestamps.append(elapsed)
            fputs("frames=\(count) elapsed=\(String(format:"%.3f",elapsed))s\n",stderr)
        }
    }
    try encoded.fileHandleForWriting.close()
    decoder.waitUntilExit()
    encoder.waitUntilExit()
    guard decoder.terminationStatus == 0, encoder.terminationStatus == 0, count == limit else {
        throw NSError(domain:"PersonMatte", code:4, userInfo:[NSLocalizedDescriptionKey:"Frame count or FFmpeg failed: \(count)/\(limit), decode \(decoder.terminationStatus), encode \(encoder.terminationStatus)"])
    }
    let elapsed=Date().timeIntervalSince(started)
    let metrics: [String:Any] = ["frames":count,"fps":fps,"width":width,"height":height,
        "crop_x":656,"crop_y":0,"duration_seconds":Double(count)/Double(fps),
        "runtime_seconds":elapsed,"processing_fps":Double(count)/elapsed,
        "request":"VNGeneratePersonSegmentationRequest","request_revision":request.revision,
        "quality":"accurate","stateful_sequence":true,"mask_pixel_format":"OneComponent8",
        "native_mask_sizes":nativeSizes.sorted(),"resize":"center-aligned bilinear",
        "postprocessing":"none","mask_black":0,"mask_white":255,"color_range":"full",
        "rgb_modified":false,"progress_elapsed_seconds":timestamps,
        "os":ProcessInfo.processInfo.operatingSystemVersionString]
    let json=try JSONSerialization.data(withJSONObject:metrics,options:[.prettyPrinted,.sortedKeys])
    try json.write(to:URL(fileURLWithPath:args[4]))
    print(String(data:json,encoding:.utf8)!)
} catch {
    fputs("PersonMatte failed: \(error)\n",stderr)
    exit(1)
}
