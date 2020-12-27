-- for col in line:gmatch("([^,]+)") do
--     mp.osd_message(col)
-- end
local path = "D:\\Arquivos de Programa\\mpv\\data_"..os.date("%Y")..".csv"

local timer = nil
local start = -1;

local begin = 
{
    year = -1,
    month = -1,
    day = -1,
    hour = -1,
    minute = -1,
    date = "",
    time = ""
}
local duration = -1
local title = ""

local addEpisode = true

function get_file_data()
    addEpisode = true
    start = os.time()

    begin.year = tonumber(os.date("%y"))
    begin.month = tonumber(os.date("%m"))
    begin.day = tonumber(os.date("%d"))
    begin.hour = tonumber(os.date("%H"))
    begin.minute = tonumber(os.date("%M"))
    begin.date = os.date("%x")
    begin.time = os.date("%X")

    duration = mp.get_property_number("duration", -1)

    title = mp.get_property("media-title", "")
    title = title:gsub('%b[]', '')--remove []
    title = title:gsub('%b()', '')--remove ()
    if title:match('%..+') ~= nil then -- remove file extension
        title = title:match('(.+)%..+') 
    end
    if title:sub(1,1) == " " then -- remove first blank space
        title = title:sub(2,title:len())
    end
    local len = title:len()
    if title:sub(len,len) == " " then -- remove last blank space
        title = title:sub(1,len-1)
    end
    
    for line in io.lines(path) do
        local name, rest = line:match("([^,]+)")
        if name == title then 
            addEpisode = false
            break
        end
    end

    if addEpisode then
        --mp.observe_property("time-pos", "number", automatic_add)
        timer = mp.add_periodic_timer(1, automatic_add)
    end

    mp.add_key_binding("'", "manual_add", manual_add)
end

function add_episode()
    local file = io.open(path, "a+")
    file:write(title..","..
                duration..","..
                begin.day..","..
                begin.month..","..
                begin.year..","..
                begin.hour..","..
                begin.minute..","..
                begin.date..","..
                begin.time..","..
                tonumber(os.date("%d"))..","..
                tonumber(os.date("%m"))..","..
                tonumber(os.date("%y"))..","..
                tonumber(os.date("%H"))..","..
                tonumber(os.date("%M"))..","..
                os.date("%x")..","..
                os.date("%X").."\n")
    file:close()
    addEpisode = false

    mp.osd_message("Data tracked")
end

function automatic_add()
    local timeSpent = os.time() - start
    local time = mp.get_property_number("time-pos", -1)

    local PercentageWatched = time/duration
    local PercentageSpent = timeSpent/duration
    mp.osd_message(PercentageWatched)
    if PercentageWatched >= 0.8 and PercentageSpent >= 0.2 then
    --if PercentageWatched >= 0.8 then
        --mp.unobserve_property(automatic_add)
        timer:kill()
        add_episode()
    end
end

function manual_add()
    if addEpisode then
        add_episode()
    else
        mp.osd_message("Data alredy tracked")
    end
end

mp.register_event("file-loaded", get_file_data)

