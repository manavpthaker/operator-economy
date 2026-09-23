-- Run in Resolve console (project OE_EP007). Builds EP007_R81_MASTER (R81 edit + -14 LUFS dialogue mix) and queues two renders.
local H = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r81-cut-never-sold/"
local edl = dofile(H .. "_tools/r81_edl.lua")
local mix = "/Users/brownmanbrain/Movies/OE/EP007-r81/ep007-r81-mix-14lufs.wav"
local outdir = "/Users/brownmanbrain/Movies/OE/EP007-masters"
local pm = resolve:GetProjectManager()
local proj = pm:GetCurrentProject()
local mp = proj:GetMediaPool()
local byPath = {}
local function walk(f) for _, it in ipairs(f:GetClipList()) do byPath[it:GetClipProperty("File Path")] = it end for _, s in ipairs(f:GetSubFolderList()) do walk(s) end end
walk(mp:GetRootFolder())
local need = {}
if not byPath[mix] then need[#need + 1] = mix end
for _, c in ipairs(edl) do if not byPath[c.path] then need[#need + 1] = c.path end end
if #need > 0 then for _, it in ipairs(mp:ImportMedia(need) or {}) do byPath[it:GetClipProperty("File Path")] = it end end
for i = proj:GetTimelineCount(), 1, -1 do local t = proj:GetTimelineByIndex(i); if t:GetName() == "EP007_R81_MASTER" then mp:DeleteTimelines({t}) end end
local tl = mp:CreateEmptyTimeline("EP007_R81_MASTER")
proj:SetCurrentTimeline(tl)
local st = tl:GetStartFrame()
for _, c in ipairs(edl) do
  mp:AppendToTimeline({{mediaPoolItem = byPath[c.path], startFrame = c.a, endFrame = c.b, mediaType = 1, trackIndex = 1, recordFrame = st + c.rec}})
end
mp:AppendToTimeline({{mediaPoolItem = byPath[mix], mediaType = 2, trackIndex = 1, recordFrame = st}})
print("master timeline v1 " .. #tl:GetItemListInTrack("video", 1) .. " end " .. (tl:GetEndFrame() - st))
tl:Export(H .. "finishing/master-timeline.otio", resolve.EXPORT_OTIO, resolve.EXPORT_NONE)
proj:DeleteAllRenderJobs()
local function job(fmt, codec, name, extra)
  print(name .. " fmt " .. tostring(proj:SetCurrentRenderFormatAndCodec(fmt, codec)))
  local s = {SelectAllFrames = true, TargetDir = outdir, CustomName = name, ExportVideo = true, ExportAudio = true,
             FormatWidth = 1920, FormatHeight = 1080, FrameRate = 24, AudioSampleRate = 48000}
  for k, v in pairs(extra) do s[k] = v end
  print(name .. " settings " .. tostring(proj:SetRenderSettings(s)))
  print(name .. " job " .. tostring(proj:AddRenderJob()))
end
job("mp4", "H264", "EP007_R81_upload_1080p24", {VideoQuality = 40000, AudioCodec = "aac", AudioBitDepth = 16})
job("mov", "ProRes422", "EP007_R81_archive_1080p24_prores422", {AudioCodec = "lpcm", AudioBitDepth = 24})
pm:SaveProject()
print("rendering " .. tostring(proj:StartRendering()))
