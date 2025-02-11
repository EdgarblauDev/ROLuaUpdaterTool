def get_iteminfo_function():
    """Get the iteminfo function modified to display the item without needing a magnifier"""

    data = """

dofile("System/customeffects.lua")
dofile("System/customsprites.lua")
dofile("System/customweapon.lua")

main = function()
    for ItemID, DESC in pairs(tbl) do
        local unidentifiedDisplayName = "";
        
        if DESC.slotCount ~= nil and DESC.slotCount > 0 then
            unidentifiedDisplayName = DESC.identifiedDisplayName .. " [" .. DESC.slotCount .. "]";
        else
            unidentifiedDisplayName = DESC.identifiedDisplayName;
        end

		--customsprites code starts here
		local identifiedResourceName = "";

		if customsprites[ItemID] ~= nil then
		  identifiedResourceName = customsprites[ItemID];
		else
		  identifiedResourceName = DESC.identifiedResourceName;
		end

        --customweapon
        local ClassNum = 0;

        if customweapon[ItemID] ~= nil then
            ClassNum = customweapon[ItemID];
        else
            ClassNum = DESC.ClassNum;
        end
        --customweapon code ends here

		result, msg = AddItem(ItemID, unidentifiedDisplayName, identifiedResourceName, DESC.identifiedDisplayName, identifiedResourceName, DESC.slotCount, ClassNum)		
		--customsprites code ends here

        if not result == true then
            return false, msg
        end
        
        for k, v in pairs(DESC.identifiedDescriptionName) do
            result, msg = AddItemIdentifiedDesc(ItemID, v)
            result, msg = AddItemUnidentifiedDesc(ItemID, v)
            if not result == true then
                return false, msg
            end
        end

        if nil ~= DESC.EffectID then
			result, msg = AddItemEffectInfo(ItemID, DESC.EffectID)
			if not result == true then
				return false, msg
			end
		end
        k = DESC.identifiedResourceName
        v = DESC.identifiedDisplayName
    end
    
    -- add user defined effects
    for ItemID, DESC in pairs(customeffects) do
        result, msg = AddItemEffectInfo(ItemID, DESC.EffectID)
        if not result == true then
            return false, msg
        end
    end

    return true, "good"
end
    """
    return data
