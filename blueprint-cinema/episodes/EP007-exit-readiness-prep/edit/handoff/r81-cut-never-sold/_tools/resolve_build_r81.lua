-- Run in Resolve console (project OE_EP007): builds EP007_R81_CONFORM from R80 plates per EDIT-LIST (owner cut of "I have never sold a business.").
local edl = dofile("/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r81-cut-never-sold/_tools/r81_edl.lua")
local wav = os.getenv("HOME") .. "/Movies/OE/EP007-r81/ep007-r81-audio-pcm.wav"
local proj = resolve:GetProjectManager():GetCurrentProject()
local mp = proj:GetMediaPool()
local byPath = {}
local function walk(f) for _, it in ipairs(f:GetClipList()) do byPath[it:GetClipProperty("File Path")] = it end for _, s in ipairs(f:GetSubFolderList()) do walk(s) end end
walk(mp:GetRootFolder())
local need = {}
if not byPath[wav] then need[#need + 1] = wav end
for _, c in ipairs(edl) do if not byPath[c.path] then need[#need + 1] = c.path end end
if #need > 0 then for _, it in ipairs(mp:ImportMedia(need) or {}) do byPath[it:GetClipProperty("File Path")] = it end end
for i = 1, proj:GetTimelineCount() do local t = proj:GetTimelineByIndex(i); if t:GetName() == "EP007_R81_CONFORM" then mp:DeleteTimelines({t}) break end end
local tl = mp:CreateEmptyTimeline("EP007_R81_CONFORM")
proj:SetCurrentTimeline(tl)
local st = tl:GetStartFrame()
local missing = 0
for _, c in ipairs(edl) do
  local it = byPath[c.path]
  if it then mp:AppendToTimeline({{mediaPoolItem = it, startFrame = c.a, endFrame = c.b, mediaType = 1, trackIndex = 1, recordFrame = st + c.rec}}) else missing = missing + 1 end
end
mp:AppendToTimeline({{mediaPoolItem = byPath[wav], mediaType = 2, trackIndex = 1, recordFrame = st}})
print("R81 v1 " .. #tl:GetItemListInTrack("video", 1) .. " missing " .. missing .. " end " .. (tl:GetEndFrame() - st))
local out = "/Users/brownmanbrain/GitHub/operator-economy/blueprint-cinema/episodes/EP007-exit-readiness-prep/edit/handoff/r81-cut-never-sold/interchange/"
print("otio " .. tostring(tl:Export(out .. "timeline.otio", resolve.EXPORT_OTIO, resolve.EXPORT_NONE)))
print("edl " .. tostring(tl:Export(out .. "timeline.edl", resolve.EXPORT_EDL, resolve.EXPORT_NONE)))
print("saved " .. tostring(resolve:GetProjectManager():SaveProject()))
