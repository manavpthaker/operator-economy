import Foundation
import Vision
import ImageIO

// Diagnostic only. Input PNGs are the source crop full frame normalized to 1280x720.
var rows: [[String: Any]] = []
for path in CommandLine.arguments.dropFirst() {
    guard let source=CGImageSourceCreateWithURL(URL(fileURLWithPath:path) as CFURL,nil),
          let image=CGImageSourceCreateImageAtIndex(source,0,nil) else { exit(2) }
    let request=VNDetectFaceLandmarksRequest()
    try VNImageRequestHandler(cgImage:image,orientation:.up).perform([request])
    guard let face=request.results?.max(by:{$0.boundingBox.width < $1.boundingBox.width}),
          let landmarks=face.landmarks else { exit(3) }
    let bx=Double(face.boundingBox.minX), by=Double(face.boundingBox.minY)
    let bw=Double(face.boundingBox.width), bh=Double(face.boundingBox.height)
    let w=Double(image.width), h=Double(image.height)
    var points: [String:[[Double]]] = [:]
    for (name,region) in ["left_eye":landmarks.leftEye,"right_eye":landmarks.rightEye,"nose":landmarks.nose,"face_contour":landmarks.faceContour] {
        guard let region else { continue }
        var pp: [[Double]] = []
        for p in region.normalizedPoints {
            let x=(bx+Double(p.x)*bw)*w
            let y=(1.0-by-Double(p.y)*bh)*h
            pp.append([x,y])
        }
        points[name]=pp
    }
    rows.append(["path":path,"confidence":face.confidence,"points_full_frame":points,
                 "face_bbox_full_frame_xywh":[bx*w,(1.0-by-bh)*h,bw*w,bh*h]])
}
let data=try JSONSerialization.data(withJSONObject:rows,options:[.prettyPrinted,.sortedKeys])
print(String(data:data,encoding:.utf8)!)
