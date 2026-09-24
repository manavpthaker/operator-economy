-- Rebuild EP007_R80_CONFORM from already-imported media. endFrame is exclusive in AppendToTimeline.
local plates = dofile("/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/_tools/r80_plates.lua")
local pcm = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/assembly/r79-full-conform/qa/ep007-r79-audio-pcm.wav"
local proj = resolve:GetProjectManager():GetCurrentProject()
local mp = proj:GetMediaPool()
local byPath = {}
local function walk(folder)
  for _, it in ipairs(folder:GetClipList()) do byPath[it:GetClipProperty("File Path")] = it end
  for _, sub in ipairs(folder:GetSubFolderList()) do walk(sub) end
end
walk(mp:GetRootFolder())
local old = {}
for i = 1, proj:GetTimelineCount() do old[#old + 1] = proj:GetTimelineByIndex(i) end
mp:DeleteTimelines(old)
local tl = mp:CreateEmptyTimeline("EP007_R80_CONFORM")
proj:SetCurrentTimeline(tl)
local start = tl:GetStartFrame()
local missing = 0
for _, p in ipairs(plates) do
  local it = byPath[p.path]
  if it then mp:AppendToTimeline({{mediaPoolItem = it, startFrame = 0, endFrame = p.b - p.a, mediaType = 1, trackIndex = 1, recordFrame = start + p.a}}) else missing = missing + 1 end
end
mp:AppendToTimeline({{mediaPoolItem = byPath[pcm], mediaType = 2, trackIndex = 1, recordFrame = start}})
print("rebuilt timelines " .. proj:GetTimelineCount() .. " missing " .. missing .. " v1 " .. #tl:GetItemListInTrack("video", 1) .. " end " .. (tl:GetEndFrame() - start))
local out = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/interchange/"
print("otio " .. tostring(tl:Export(out .. "timeline.otio", resolve.EXPORT_OTIO, resolve.EXPORT_NONE)))
print("fcpxml " .. tostring(tl:Export(out .. "timeline.fcpxml", resolve.EXPORT_FCPXML_1_10, resolve.EXPORT_NONE)))
print("edl " .. tostring(tl:Export(out .. "timeline.edl", resolve.EXPORT_EDL, resolve.EXPORT_NONE)))
print("saved " .. tostring(resolve:GetProjectManager():SaveProject()))
