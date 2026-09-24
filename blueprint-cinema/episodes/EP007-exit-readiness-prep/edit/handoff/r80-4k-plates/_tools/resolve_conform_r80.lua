-- Run inside DaVinci Resolve (Workspace > Console, Lua): dofile("<abs path>/resolve_conform_r80.lua")
-- Builds timeline EP007_R80_CONFORM from the R80 1080p plates + locked R79 PCM. endFrame is exclusive.
local base = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r80-4k-plates/"
local plates = dofile(base .. "_tools/r80_plates.lua")
local pcm = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/experiments/EP007-NET-NEW-UNFINISHED-ANSWER-003/assembly/r79-full-conform/qa/ep007-r79-audio-pcm.wav"
local pm = resolve:GetProjectManager()
local proj = pm:GetCurrentProject()
assert(proj:GetName() == "OE_EP007", "open project OE_EP007 first")
for k, v in pairs({timelineFrameRate="24", timelinePlaybackFrameRate="24", timelineResolutionWidth="1920", timelineResolutionHeight="1080", videoMonitorFormat="HD 1080p 24"}) do
  proj:SetSetting(k, v)
end
local mp = proj:GetMediaPool()
local root = mp:GetRootFolder()
local bin = mp:AddSubFolder(root, "R80_plates") or root
mp:SetCurrentFolder(bin)
local paths = {}
for i, p in ipairs(plates) do paths[i] = p.path end
paths[#paths + 1] = pcm
local items = mp:ImportMedia(paths)
local byPath = {}
for _, it in ipairs(items) do byPath[it:GetClipProperty("File Path")] = it end
local tl = mp:CreateEmptyTimeline("EP007_R80_CONFORM")
proj:SetCurrentTimeline(tl)
local start = tl:GetStartFrame()
local report = {timeline_start = start, clips = {}, missing = {}}
for _, p in ipairs(plates) do
  local it = byPath[p.path]
  if not it then table.insert(report.missing, p.path) else
    mp:AppendToTimeline({{mediaPoolItem = it, startFrame = 0, endFrame = p.b - p.a, mediaType = 1, trackIndex = 1, recordFrame = start + p.a}})
  end
end
local a = byPath[pcm]
if a then mp:AppendToTimeline({{mediaPoolItem = a, mediaType = 2, trackIndex = 1, recordFrame = start}}) else table.insert(report.missing, pcm) end
for _, ti in ipairs(tl:GetItemListInTrack("video", 1)) do
  table.insert(report.clips, string.format('{"name":"%s","start":%d,"end":%d}', ti:GetName(), ti:GetStart() - start, ti:GetEnd() - start))
end
pm:SaveProject()
print("R80 conform done; verify with resolve_export_r80.lua (io is unavailable in Resolve Lua)")
