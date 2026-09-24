// Record only the explicitly selected browser window. UI actions belong to CUA.
import Foundation
import ScreenCaptureKit
import AVFoundation
import AppKit

final class RecorderDelegate: NSObject, SCRecordingOutputDelegate {
    var finished = false
    func recordingOutputDidStartRecording(_ output: SCRecordingOutput) {
        print("RECORDING_STARTED"); fflush(stdout)
    }
    func recordingOutputDidFinishRecording(_ output: SCRecordingOutput) {
        print("RECORDING_FINISHED duration=\(output.recordedDuration.seconds) bytes=\(output.recordedFileSize)")
        fflush(stdout); finished = true
    }
    func recordingOutput(_ output: SCRecordingOutput, didFailWithError error: Error) {
        print("RECORDING_ERROR \(error.localizedDescription)"); fflush(stdout); finished = true
    }
}

@main struct Capture {
    static func main() async throws {
        _ = NSApplication.shared
        let args = CommandLine.arguments
        let content = try await SCShareableContent.excludingDesktopWindows(true, onScreenWindowsOnly: false)
        let windows = content.windows.filter { $0.owningApplication?.bundleIdentifier == "com.google.Chrome" && (($0.title ?? "").contains("EP007") || ($0.title ?? "").contains("ChatGPT")) }
        if args.count < 4 {
            for w in content.windows.filter({ $0.owningApplication?.bundleIdentifier == "com.google.Chrome" }) { print("\(w.windowID)\t\(w.frame)\t\(w.title ?? "")") }
            return
        }
        guard let id = UInt32(args[1]), let window = windows.first(where: {$0.windowID == id}) else {
            throw NSError(domain: "EP007Capture", code: 1, userInfo: [NSLocalizedDescriptionKey:"Selected EP007 Chrome window is not available"])
        }
        let seconds = Double(args[3]) ?? 60
        let filter = SCContentFilter(desktopIndependentWindow: window)
        let config = SCStreamConfiguration()
        config.width = Int(window.frame.width) * 2
        config.height = Int(window.frame.height) * 2
        config.minimumFrameInterval = CMTime(value: 1, timescale: 24)
        config.queueDepth = 6
        config.showsCursor = true
        config.capturesAudio = false
        config.captureMicrophone = false
        config.ignoreShadowsSingleWindow = true
        let stream = SCStream(filter: filter, configuration: config, delegate: nil)
        let outputConfig = SCRecordingOutputConfiguration()
        outputConfig.outputURL = URL(fileURLWithPath: args[2])
        outputConfig.outputFileType = .mp4
        outputConfig.videoCodecType = .h264
        let delegate = RecorderDelegate()
        let output = SCRecordingOutput(configuration: outputConfig, delegate: delegate)
        try stream.addRecordingOutput(output)
        print("WINDOW id=\(id) width=\(config.width) height=\(config.height) seconds=\(seconds)"); fflush(stdout)
        try await stream.startCapture()
        try await Task.sleep(for: .seconds(seconds))
        try await stream.stopCapture()
        for _ in 0..<100 {
            if delegate.finished { break }
            try await Task.sleep(for: .milliseconds(100))
        }
        guard delegate.finished else { throw NSError(domain:"EP007Capture", code:2, userInfo:[NSLocalizedDescriptionKey:"Recording finalization timeout"]) }
    }
}
