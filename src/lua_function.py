def get_iteminfo_function():
    """Get the iteminfo function modified to display the item without needing a magnifier"""

    data = """

main = function()
	for ItemID, DESC in pairs(tbl) do
		result, msg = AddItem(ItemID, DESC.identifiedDisplayName, DESC.identifiedResourceName, DESC.identifiedDisplayName, DESC.identifiedResourceName, DESC.slotCount, DESC.ClassNum)
		if not result == true then
			return false, msg
		end
		for k, v in pairs(DESC.identifiedDescriptionName) do
        	result, msg = AddItemUnidentifiedDesc(ItemID, v)
			result, msg = AddItemIdentifiedDesc(ItemID, v)
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
	return true, "good"
end

    """
    return data
