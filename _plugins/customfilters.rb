module Jekyll
  module CustomFilters
    # @param tag_hash   Map of tag names to a list of associated posts.
    # @return           List of tag names, with most popular tags first.
    def tags_names_by_popularity(tag_hash)
      (tag_hash.sort_by {|k,v| [-v.size, k]}).map {|kv| kv[0]}
    end
    
    # My own short date format
    def usa_date_to_string(date)
      date.strftime("%b %d, %Y")
    end
  end
end

Liquid::Template.register_filter(Jekyll::CustomFilters)