on connectEverything()
	tell application "OmniGraffle Professional 4"
		set circles to get graphics of canvas 2 of document 1 where locked is false
		repeat with i from 1 to the number of items in circles
			repeat with j from i + 1 to the number of items in circles
				connect (item i of circles) to (item j of circles)
			end repeat
		end repeat
	end tell
end connectEverything

tell application "OmniGraffle Professional 4"
	set circles to get graphics of canvas 2 of document 1 where locked is false
	set publicCircles to get graphics of canvas 2 of document 1 where locked is false and thickness is 2
	
	repeat with i in circles
		repeat with j in publicCircles
			connect i to j
		end repeat
	end repeat
end tell