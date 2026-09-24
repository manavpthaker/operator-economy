import Foundation
import Vision
import ImageIO
import CoreVideo

// Geometry aid only. Generated reference face/neck is not approved for compositing.
// Usage: FaceAlignment source.png reference.png alignment.json [reference-mask.png]
let args = CommandLine.arguments
guard args.count == 4 || args.count == 5 else { exit(2) }

func writeMask(_ path: String, _ output: String) throws {
    let url=URL(fileURLWithPath:path)
    guard let src=CGImageSourceCreateWithURL(url as CFURL,nil),let image=CGImageSourceCreateImageAtIndex(src,0,nil) else { throw NSError(domain:"FaceAlignment",code:4) }
    let request=VNGeneratePersonSegmentationRequest()
    request.qualityLevel = .accurate
    request.outputPixelFormat=kCVPixelFormatType_OneComponent8
    try VNImageRequestHandler(cgImage:image,orientation:.up).perform([request])
    guard let mask=request.results?.first?.pixelBuffer else { throw NSError(domain:"FaceAlignment",code:5) }
    let w=image.width,h=image.height,mw=CVPixelBufferGetWidth(mask),mh=CVPixelBufferGetHeight(mask)
    CVPixelBufferLockBaseAddress(mask,.readOnly)
    defer { CVPixelBufferUnlockBaseAddress(mask,.readOnly) }
    let stride=CVPixelBufferGetBytesPerRow(mask)
    let pixels=CVPixelBufferGetBaseAddress(mask)!.assumingMemoryBound(to:UInt8.self)
    var data=Data(count:w*h)
    data.withUnsafeMutableBytes { bytes in
        let dest=bytes.baseAddress!.assumingMemoryBound(to:UInt8.self)
        for y in 0..<h {
            let sy=max(0,min(Double(mh-1),(Double(y)+0.5)*Double(mh)/Double(h)-0.5))
            let y0=Int(sy),y1=min(y0+1,mh-1),fy=sy-Double(y0)
            for x in 0..<w {
                let sx=max(0,min(Double(mw-1),(Double(x)+0.5)*Double(mw)/Double(w)-0.5))
                let x0=Int(sx),x1=min(x0+1,mw-1),fx=sx-Double(x0)
                let a=Double(pixels[y0*stride+x0])*(1-fx)+Double(pixels[y0*stride+x1])*fx
                let b=Double(pixels[y1*stride+x0])*(1-fx)+Double(pixels[y1*stride+x1])*fx
                dest[y*w+x]=UInt8((a*(1-fy)+b*fy).rounded())
            }
        }
    }
    let provider=CGDataProvider(data:data as CFData)!
    let gray=CGImage(width:w,height:h,bitsPerComponent:8,bitsPerPixel:8,bytesPerRow:w,space:CGColorSpaceCreateDeviceGray(),bitmapInfo:CGBitmapInfo(rawValue:0),provider:provider,decode:nil,shouldInterpolate:false,intent:.defaultIntent)!
    guard let dest=CGImageDestinationCreateWithURL(URL(fileURLWithPath:output) as CFURL,"public.png" as CFString,1,nil) else { throw NSError(domain:"FaceAlignment",code:6) }
    CGImageDestinationAddImage(dest,gray,nil)
    guard CGImageDestinationFinalize(dest) else { throw NSError(domain:"FaceAlignment",code:7) }
}

struct Face {
    let width: Int
    let height: Int
    let anchors: [String:CGPoint]
    let confidence: Float
    let faceCount: Int
}
func detect(_ path: String) throws -> Face {
    let url = URL(fileURLWithPath:path)
    guard let imageSource = CGImageSourceCreateWithURL(url as CFURL,nil),
          let cgImage = CGImageSourceCreateImageAtIndex(imageSource,0,nil) else { throw NSError(domain:"FaceAlignment",code:1) }
    let request = VNDetectFaceLandmarksRequest()
    try VNImageRequestHandler(cgImage:cgImage,orientation:.up).perform([request])
    guard let results=request.results, let face=results.max(by:{$0.boundingBox.width*$0.boundingBox.height < $1.boundingBox.width*$1.boundingBox.height}), let landmarks=face.landmarks else { throw NSError(domain:"FaceAlignment",code:2) }
    let regions: [String:VNFaceLandmarkRegion2D?] = ["left_eye":landmarks.leftEye,"right_eye":landmarks.rightEye,"nose":landmarks.nose,"nose_crest":landmarks.noseCrest]
    var anchors: [String:CGPoint] = [:]
    for (name,region) in regions {
        guard let region, region.pointCount>0 else { continue }
        let p=region.normalizedPoints
        let mx=p.map{Double($0.x)}.reduce(0,+)/Double(p.count)
        let my=p.map{Double($0.y)}.reduce(0,+)/Double(p.count)
        anchors[name]=CGPoint(x:(face.boundingBox.minX+mx*face.boundingBox.width)*Double(cgImage.width),
                             y:(1-face.boundingBox.minY-my*face.boundingBox.height)*Double(cgImage.height))
    }
    return Face(width:cgImage.width,height:cgImage.height,anchors:anchors,confidence:face.confidence,faceCount:results.count)
}
do {
    let a=try detect(args[1]),b=try detect(args[2])
    let names=a.anchors.keys.filter{b.anchors[$0] != nil}.sorted()
    guard names.count>=3 else { throw NSError(domain:"FaceAlignment",code:3) }
    let ax=names.map{a.anchors[$0]!.x}.reduce(0,+)/Double(names.count)
    let ay=names.map{a.anchors[$0]!.y}.reduce(0,+)/Double(names.count)
    let bx=names.map{b.anchors[$0]!.x}.reduce(0,+)/Double(names.count)
    let by=names.map{b.anchors[$0]!.y}.reduce(0,+)/Double(names.count)
    var numerator=0.0,denominator=0.0
    for name in names {
        let p=a.anchors[name]!,q=b.anchors[name]!
        numerator += (p.x-ax)*(q.x-bx)+(p.y-ay)*(q.y-by)
        denominator += (p.x-ax)*(p.x-ax)+(p.y-ay)*(p.y-ay)
    }
    let scale=numerator/denominator,tx=bx-scale*ax,ty=by-scale*ay
    let residuals=names.map{name -> [String:Any] in
        let p=a.anchors[name]!,q=b.anchors[name]!
        return ["name":name,"source":[p.x,p.y],"reference":[q.x,q.y],"residual_px":Double(hypot(scale*p.x+tx-q.x,scale*p.y+ty-q.y))]
    }
    let rms=sqrt(residuals.map{pow($0["residual_px"] as! Double,2)}.reduce(0,+)/Double(names.count))
    let factor=1920.0/Double(b.width)
    let result: [String:Any] = ["method":"Vision VNDetectFaceLandmarksRequest; least-squares isotropic scale and translation over eye, nose, nose-crest centroids; no rotation",
        "coordinate_system":"pixel coordinates, top left origin, x right, y down",
        "source_path":args[1],"reference_path":args[2],"source_dimensions":[a.width,a.height],"reference_dimensions":[b.width,b.height],
        "source_faces":a.faceCount,"reference_faces":b.faceCount,"source_confidence":a.confidence,"reference_confidence":b.confidence,
        "source_to_reference":["scale":scale,"translate_x":tx,"translate_y":ty],
        "reference_to_source":["scale":1/scale,"translate_x":(-tx/scale),"translate_y":(-ty/scale)],
        "source_to_reference_scaled_to_width_1920":["scale":scale*factor,"translate_x":tx*factor,"translate_y":ty*factor,"reference_scaled_height":Double(b.height)*factor],
        "anchor_rms_error_reference_px":rms,"anchors":residuals,
        "limits":["Single-frame alignment only, not tracking.","No guarantee of shoulder or collar agreement.","Generated reference face and neck must not be retained behind moving foreground.","No synthesized RGB is produced or changed by this script.","Reference aspect ratio is not exactly 16:9; 1920-wide conversion has a fractional height."]]
    let data=try JSONSerialization.data(withJSONObject:result,options:[.prettyPrinted,.sortedKeys])
    try data.write(to:URL(fileURLWithPath:args[3]))
    if args.count == 5 { try writeMask(args[2],args[4]) }
    print(String(data:data,encoding:.utf8)!)
} catch { fputs("FaceAlignment failed: \(error)\n",stderr);exit(1) }
