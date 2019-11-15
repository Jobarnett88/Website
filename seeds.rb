
require 'json'
require 'rubygems'

data = File.open("the_file.json")
read = data.read()



item = JSON.parse(read)
1.upto(item.length()) do |i| 
    b = i.to_s
    Day.create(
        title:      item[b]["title"],
        StartDate:  item[b]["StartDate"],
        StartTime:  item[b]["StartTime"],
        Enddate:    item[b]["EndDate"],
        Endtime:    item[b]["EndTime"],
        category:   item[b]["Category"],
        eventdesc:  item[b]["EventDesc"],
        location:   item[b]["location"]
    )
        
end
              



