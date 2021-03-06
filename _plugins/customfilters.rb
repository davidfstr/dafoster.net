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
    
    def date_to_time(date)
      date.to_time
    end
    
    def break_after_underscores(underscore_cased_word)
      underscore_cased_word.gsub('_', '\_<wbr/>')
    end
    
    def projects_by_title(site_pages)
      site_pages.select{|p| p.data["layout"] == "project"}.sort_by{|p| p.data["title"]}
    end
    
    def projects_by_date(site_pages)
      site_pages.select{|p| p.data["layout"] == "project"}.sort_by{|p| p.data["started_on"]}.reverse
    end
    
    def posts_by_date_and_updated_date(site_posts)
      created_posts = site_posts.map do |p|
        { "type" => "created", "date" => p.date, "post" => p }
      end
      updated_posts = site_posts.select{|p| p.data["date_updated"] != nil}.map do |p|
        { "type" => "updated", "date" => p.data["date_updated"].to_time, "post" => p }
      end
      mixed_posts = (created_posts + updated_posts).sort_by{|mp| mp["date"]}
      return mixed_posts.reverse
    end
  end
end

Liquid::Template.register_filter(Jekyll::CustomFilters)


module Jekyll
  class LongUrl < Liquid::Tag

    def initialize(tag_name, text, tokens)
      super
      @text = text
    end

    def render(context)
      "<a href=\"#{@text}\">#{@text.gsub('/', '/<wbr/>')}</a>"
    end
  end
end

Liquid::Template.register_tag('long_url', Jekyll::LongUrl)
