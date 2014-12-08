
local nonvegan_labors = {
    "BUTCHER",
    "TRAPPER",
    "DISSECT_VERMIN",
    "LEATHER",
    "TANNER",
    "MAKE_CHEESE",
    "MILK",
    "FISH",
    "CLEAN_FISH",
    "DISSECT_FISH",
    "HUNT",
    "BONE_CARVE",
    "SHEARER",
    "BEEKEEPING",
    "WAX_WORKING",
    "GELD",
}

for i, labor in ipairs(nonvegan_labors) do
    dfhack.run_command(string.format("autolabor %s 0 0", labor))
end
