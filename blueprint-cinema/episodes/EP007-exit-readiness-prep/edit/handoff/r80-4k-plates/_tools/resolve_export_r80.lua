-- Run in Resolve console after resolve_conform_r80.lua. Saves project, reports timelines, exports interchange.
local proj = resolve:GetProjectManager():GetCurrentProject()
local n = proj:GetTimelineCount()
local names = {}
for i = 1, n do names[#names + 1] = proj:GetTimelineByIndex(i):GetName() end
print("timelines: " .. n .. " -> " .. table.concat(names, ", "))
local tl = proj:GetCurrentTimeline()
print("current: " .. tl:GetName() .. " start " .. tl:GetStartFrame() .. " end " .. tl:GetEndFrame() .. " v1 clips " .. #tl:GetItemListInTrack("video", 1) .. " a1 clips " .. #tl:GetItemListInTrack("audio", 1))
print("mediapool root clips: " .. #proj:GetMediaPool():GetRootFolder():GetClipList())
local out = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/interchange/"
print("fcpxml " .. tostring(tl:Export(out .. "timeline.fcpxml", resolve.EXPORT_FCPXML_1_10, resolve.EXPORT_NONE)))
print("otio " .. tostring(tl:Export(out .. "timeline.otio", resolve.EXPORT_OTIO, resolve.EXPORT_NONE)))
print("edl " .. tostring(tl:Export(out .. "timeline.edl", resolve.EXPORT_EDL, resolve.EXPORT_NONE)))
print("saved " .. tostring(resolve:GetProjectManager():SaveProject()))
