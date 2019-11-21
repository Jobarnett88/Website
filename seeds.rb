# This file should contain all the record creation needed to seed the database with its default values.
# The data can then be loaded with the rails db:seed command (or created alongside the database with db:setup).
#
# Examples:
#
#   movies = Movie.create([{ name: 'Star Wars' }, { name: 'Lord of the Rings' }])
#   Character.create(name: 'Luke', movie: movies.first)
require 'json'
require 'rubygems'

data = File.open("the_file.json")
read = data.read()

@locations = Location.all
@types = Type.all

item = JSON.parse(read)
1.upto(item.length()) do |i|
    b = i.to_s
    Event.create(
        title:      item[b]["title"],
        day:  item[b]["StartDate"],
        stime:  item[b]["StartTime"],
        enddate:    item[b]["EndDate"],
        endtime:    item[b]["EndTime"],
        @types.each do |type|
          temp = Type.find(item[b]["Category"] = type.name)
        end,
        Type_id: temp.id,
        eventdesc:  item[b]["EventDesc"],
        @locations.each do |location|
          temp2 = Location.find(item[b]["Location"] = location.name)
        end
        Location_id: (temp2.id)

    )

end
