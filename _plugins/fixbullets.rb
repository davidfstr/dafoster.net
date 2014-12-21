BULLET_CHARS = ["*", "+", "-"]

module Jekyll
  module BulletFixerFilter
    # Fix rendering of bulleted lists that have variable spacing
    # between list items.
    def fixbullets(text)
      BulletFixer.new.scan text
    end
  end
end

Liquid::Template.register_filter(Jekyll::BulletFixerFilter)

### BulletFixer ###

class BulletFixer
  ### Scan ###
  
  def scan input
    @output_lines = []
    inside_list = false
    @last_bullet_indentation = -1
    @last_bullet_lines = []
    
    input.lines.each do |cur_input_line|
      if not inside_list
        cur_bullet_indentation = get_bullet_line_indentation cur_input_line
        if cur_bullet_indentation == -1
          # Line outside list
          @output_lines << cur_input_line
        else
          # Start list
          inside_list = true
          
          # Start new bullet
          @last_bullet_indentation = cur_bullet_indentation
          @last_bullet_lines = [cur_input_line]
        end
      else
        cur_bullet_indentation = get_bullet_line_indentation cur_input_line
        if cur_bullet_indentation == -1
          if is_whitespace cur_input_line[0..(@last_bullet_indentation-1)]
            # Continue last bullet
            @last_bullet_lines << cur_input_line
          else
            # End last bullet
            end_last_bullet false
            
            # End list
            inside_list = false
            
            # Line outside list
            @output_lines << cur_input_line
          end
        else
          # End last bullet
          end_last_bullet true
          
          # Start new bullet
          @last_bullet_indentation = cur_bullet_indentation
          @last_bullet_lines = [cur_input_line]
        end
      end
    end
    
    if inside_list
      end_last_bullet false
    end
    
    @output_lines.join("")
  end
  
  def get_bullet_line_indentation line
    stripped = line.strip
    if stripped.size >= 2 and BULLET_CHARS.include? stripped[0] and stripped[1] == ' '
      # Assume that there is exactly one whitespace char between
      # bullet and its line's content
      line.scan(/^\s*/)[0].size + 2
    else
      -1
    end
  end

  def end_last_bullet next_line_is_bullet
    if next_line_is_bullet
      # Check whether last bullet's needs to be given an extra <p></p> wrapper
      # to render correctly in Markdown in the presence of variable vertical
      # spacing between bullets.
      if @last_bullet_lines.size >= 1 and is_whitespace @last_bullet_lines[-1]
        @last_bullet_lines = @last_bullet_lines[0..(-1-1)]
        
        # Add <p> prefix to first bullet line
        @last_bullet_lines[0] = 
          @last_bullet_lines[0][0..(@last_bullet_indentation-1)] +
          '<p>' +
          @last_bullet_lines[0][@last_bullet_indentation..-1]
        
        # Add </p> suffix to last bullet line, before trailing newline
        @last_bullet_lines[-1] = 
          @last_bullet_lines[-1][0..(-1-1)] + 
          '</p>' +
          @last_bullet_lines[-1][-1]
      end
    end
    
    # Output last bullet's lines
    @last_bullet_lines.each do |x|
      @output_lines << x
    end
  end
  
  def is_whitespace line
    line.strip == ""
  end
  
  ### Test ###
  
  def self.test
    input = """
    Hello World

    * Item 1
        - Subitem 1.1

    * Item 2
        - Subitem 2.1
        - Subitem 2.2
          has multiple lines.

    * Item 3

    * Item 4

    End World
    """

    expectedOutput = """
    Hello World

    * Item 1
        - <p>Subitem 1.1</p>
    * Item 2
        - Subitem 2.1
        - <p>Subitem 2.2
          has multiple lines.</p>
    * <p>Item 3</p>
    * Item 4

    End World
    """
    
    (BulletFixer.new.scan input) == expectedOutput
  end
end

if not BulletFixer.test
  raise "BulletFixer.scan has failed its unit test"
end