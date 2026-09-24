import Foundation
import Vision
import ImageIO

// Read-only image measurement; generated outputs are diagnostic, not approval.
var rows: [[String: Any]] = []
for path in CommandLine.arguments.dropFirst() {
    guard let source = CGImageSourceCreateWithURL(URL(fileURLWithPath:path) as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else { exit(2) }
    let request = VNDetectFaceLandmarksRequest()
    try VNImageRequestHandler(cgImage:image, orientation:.up).perform([request])
    guard let face = request.results?.max(by: {$0.boundingBox.width < $1.boundingBox.width}),
          let landmarks = face.landmarks else { exit(3) }
    let regions: [String: VNFaceLandmarkRegion2D?] = [
        "left_eye": landmarks.leftEye, "right_eye": landmarks.rightEye,
        "inner_lips": landmarks.innerLips, "outer_lips": landmarks.outerLips,
        "left_eyebrow": landmarks.leftEyebrow, "right_eyebrow": landmarks.rightEyebrow
    ]
    var points: [String: [[Double]]] = [:]
    for (name, region) in regions {
        guard let region else { continue }
        var coordinates: [[Double]] = []
        let bx = Double(face.boundingBox.minX), by = Double(face.boundingBox.minY)
        let bw = Double(face.boundingBox.width), bh = Double(face.boundingBox.height)
        for p in region.normalizedPoints {
            let x: Double = (bx + Double(p.x) * bw) * Double(image.width)
            let y: Double = (1.0 - by - Double(p.y) * bh) * Double(image.height)
            coordinates.append([x, y])
        }
        points[name] = coordinates
    }
    rows.append(["path":path, "width":image.width, "height":image.height,
                 "confidence":face.confidence, "points":points])
}
let data = try JSONSerialization.data(withJSONObject:rows, options:[.prettyPrinted, .sortedKeys])
print(String(data:data, encoding:.utf8)!)
