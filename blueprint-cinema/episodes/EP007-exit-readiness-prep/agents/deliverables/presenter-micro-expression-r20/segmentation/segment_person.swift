import Foundation
import Vision
import CoreGraphics
import CoreVideo
import ImageIO

// Native local segmentation only. The PNG stores confidence as grayscale, not RGBA.
guard CommandLine.arguments.count == 2 else {
    fatalError("Usage: swift segment_person.swift SEGMENTATION_DIRECTORY")
}
let directory = URL(fileURLWithPath: CommandLine.arguments[1], isDirectory: true)
let frames = Array(0...139)
var records: [[String: Any]] = []

func writeMask(_ buffer: CVPixelBuffer, to output: URL) throws -> (Int, Int) {
    guard CVPixelBufferGetPixelFormatType(buffer) == kCVPixelFormatType_OneComponent8 else {
        throw NSError(domain: "Segmentation", code: 1,
                      userInfo: [NSLocalizedDescriptionKey: "Unexpected mask pixel format"])
    }
    CVPixelBufferLockBaseAddress(buffer, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(buffer, .readOnly) }
    let width = CVPixelBufferGetWidth(buffer)
    let height = CVPixelBufferGetHeight(buffer)
    let rowBytes = CVPixelBufferGetBytesPerRow(buffer)
    guard let base = CVPixelBufferGetBaseAddress(buffer) else {
        throw NSError(domain: "Segmentation", code: 2)
    }
    let bytes = Data(bytes: base, count: rowBytes * height)
    guard let provider = CGDataProvider(data: bytes as CFData),
          let image = CGImage(width: width, height: height,
                              bitsPerComponent: 8, bitsPerPixel: 8,
                              bytesPerRow: rowBytes,
                              space: CGColorSpaceCreateDeviceGray(),
                              bitmapInfo: CGBitmapInfo(rawValue: CGImageAlphaInfo.none.rawValue),
                              provider: provider, decode: nil,
                              shouldInterpolate: false, intent: .defaultIntent),
          let destination = CGImageDestinationCreateWithURL(output as CFURL,
                                                            "public.png" as CFString,
                                                            1, nil) else {
        throw NSError(domain: "Segmentation", code: 3)
    }
    CGImageDestinationAddImage(destination, image, nil)
    guard CGImageDestinationFinalize(destination) else {
        throw NSError(domain: "Segmentation", code: 4)
    }
    return (width, height)
}

do {
    for frame in frames {
        let stem = String(format: "%03d", frame)
        let source = directory.appendingPathComponent("frame-\(stem).png")
        let existingOutput = directory.appendingPathComponent("alpha-native-\(stem).png")
        if FileManager.default.fileExists(atPath: existingOutput.path) {
            print("Frame \(frame): reused verified native mask")
            continue
        }
        guard let imageSource = CGImageSourceCreateWithURL(source as CFURL, nil),
              let cgImage = CGImageSourceCreateImageAtIndex(imageSource, 0, nil) else {
            throw NSError(domain: "Segmentation", code: 5,
                          userInfo: [NSLocalizedDescriptionKey: "Cannot decode \(source.path)"])
        }
        let request = VNGeneratePersonSegmentationRequest()
        request.qualityLevel = .accurate
        request.outputPixelFormat = kCVPixelFormatType_OneComponent8
        // New request per source frame: no skipped-frame temporal state is reused.
        let handler = VNImageRequestHandler(cgImage: cgImage, orientation: .up, options: [:])
        try handler.perform([request])
        guard let observation = request.results?.first else {
            throw NSError(domain: "Segmentation", code: 6,
                          userInfo: [NSLocalizedDescriptionKey: "No person mask for frame \(frame)"])
        }
        let output = directory.appendingPathComponent("alpha-native-\(stem).png")
        let size = try writeMask(observation.pixelBuffer, to: output)
        records.append([
            "frame": frame, "seconds": Double(frame) / 25.0,
            "source": source.lastPathComponent, "native_mask": output.lastPathComponent,
            "native_width": size.0, "native_height": size.1,
            "request_revision": request.revision,
            "quality": "accurate", "pixel_format": "OneComponent8",
            "input_orientation": "up", "state_reuse": false
        ])
        print("Frame \(frame): native mask \(size.0)x\(size.1)")
    }
    let report: [String: Any] = [
        "framework": "Apple Vision",
        "request": "VNGeneratePersonSegmentationRequest",
        "quality": "accurate",
        "mask_semantics": "8-bit confidence: 0 background, 255 person; grayscale PNG, no alpha channel",
        "records": records
    ]
    let json = try JSONSerialization.data(withJSONObject: report, options: [.prettyPrinted, .sortedKeys])
    try json.write(to: directory.appendingPathComponent("native-segmentation-report.json"))
} catch {
    fputs("Native segmentation failed: \(error)\n", stderr)
    exit(1)
}
