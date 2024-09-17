#child/button need no pos to create
#child sets width querying parent available width
#then child is added to parent
#parent.addchild calls child.setpos and child.setparent

#panel has no border, no margin
#panel has padding between sub panels
#panel has padding between items
#other containers have border, margin and padding between items

#convention to create gui items:
#first create parent item
#then create child item
#then adjust width of child
#querying parent's width
#then add child to parent

#normal creation pattern
#parent/panel.constructor
#child.constructor
#child.set_w
#parent.addchild(child)
#    child.set_pos
#    child.set_parent
#grandchild.constructor
#grandchild.set_w
#child.addchild(grandchild)
#    grandchild.set_pos
#    grandchild.set_parent


#story of text and button
#text.constructor called inside button.constructor
#text.set_w was not necessary because, text goes on printing till the button width allows
#button.addchild(text) was not necessary, text is not child of button
#text.set_pos called inside button.setpos, this is important
#text.set_parent called inside button.constructor, this is necessary, text needs parent width while printing
#now text and button has a weak parent child relationship

#important:
#panel get_available_w() gives available width for child
#which is without pad at beginning and pad at end
#but panel available_w has one pad to help addchild function loop.
#same for panel get_available_h() and panel available_h


# 1 - Import packages
import pygame
import sys
from io import StringIO #use strings as file
import pdb

class i_draw:
    def draw(self, surface):
        raise NotImplementedError

class text(i_draw):
    #class static variables goes before __init__
    font_surface = pygame.image.load('good_font_10x10_0space.png')
    font_newline_surface = pygame.image.load('newline_10x10.png')
    font_chars = ' !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    font_start_x = 0
    font_char_spacing = 0
    font_w = 10
    font_h = 10

    #font_color=(0, 0, 0)
    font_bgcolor=(255, 255, 255)

    def __init__(self):
        self.txt = ""
        self.parent = None

        self.x = 0
        self.y = 0

    def __blit_text(self, target_surface):
        x = self.x
        y = self.y
        parent_w = self.parent.get_content_w()
        for char in self.txt:
            if char in text.font_chars:
                # Calculate the x position of the character on the sprite sheet
                char_index = text.font_chars.index(char)
                char_x = text.font_start_x + (char_index * text.font_w) + (char_index * text.font_char_spacing)

                char_rect = pygame.Rect(char_x, 0, text.font_w, text.font_h)

                # Draw the background color as a filled rectangle behind the character
                bg_rect = pygame.Rect(x, y, text.font_w, text.font_h)
                pygame.draw.rect(target_surface, text.font_bgcolor, bg_rect)

                # Blit the character onto a new surface with per-pixel alpha enabled
                char_surface = pygame.Surface((text.font_w, text.font_h), pygame.SRCALPHA)
                char_surface.blit(text.font_surface, (0, 0), char_rect)

                # Blit the character surface to the target surface
                target_surface.blit(char_surface, (x, y))

                # Move x to the next position where to print next character
                x += text.font_w
                if x > self.x + parent_w - text.font_w:
                    break;
            elif char == '\n':
                char_rect = pygame.Rect(0, 0, text.font_w, text.font_h)

                # Draw the background color as a filled rectangle behind the character
                bg_rect = pygame.Rect(x, y, text.font_w, text.font_h)
                pygame.draw.rect(target_surface, text.font_bgcolor, bg_rect)

                # Blit the character onto a new surface with per-pixel alpha enabled
                char_surface = pygame.Surface((text.font_w, text.font_h), pygame.SRCALPHA)
                char_surface.blit(text.font_newline_surface, (0, 0), char_rect)

                # Blit the character surface to the target surface
                target_surface.blit(char_surface, (x, y))

                # Move x to the next position where to print next character
                x += text.font_w
                if x > self.x + parent_w - text.font_w:
                    break;
            else:
                print(f"Character '{char}' not in font character set.")

    def draw(self, surface):
        self.__blit_text(surface)

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_parent(self, parent):
        self.parent = parent

    def set_val(self, txt):
        self.txt = txt

class button(i_draw):
    #class static variables goes before __init__
    border = 1
    border_color = (0, 0, 0)
    margin = 1
    margin_color = (255, 255, 255)

    num_chars = 7

    @staticmethod
    def width(num_chars):
        return num_chars * text.font_w + button.border*2+button.margin*2

    @staticmethod
    def height():
        return 1 * text.font_h + button.border*2+button.margin*2

    def __init__(self, num_chars=num_chars):
        self.num_chars = num_chars
        self.txt = ""
        self.parent = None
        #do text.construct
        #do text.set_parent
        self.o_text = text()
        self.o_text.set_parent(self)

        self.x = 0
        self.y = 0
        self.w = button.width(self.num_chars)
        self.h = button.height()

        self.content_x = self.x+button.border+button.margin
        self.content_y = self.y+button.border+button.margin
        self.content_w = self.w-button.border*2-button.margin*2
        self.content_h = self.h-button.border*2-button.margin*2

        self.callback = None

    def __draw_border(self, surface):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.line(surface, BLACK, (x, y), (x+w-1, y))
        pygame.draw.line(surface, BLACK, (x+w-1, y), (x+w-1, y+h-1))
        pygame.draw.line(surface, BLACK, (x+w-1, y+h-1), (x, y+h-1))
        pygame.draw.line(surface, BLACK, (x, y+h-1), (x, y))

    def __draw_margin(self, surface):
        pass

    def draw(self, surface):
        self.__draw_border(surface)
        self.__draw_margin(surface)
        self.o_text.draw(surface)

    def size(self):
        return self.w, self.h

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.content_x = self.x+button.border+button.margin
        self.content_y = self.y+button.border+button.margin
        #special: only button has to do text.setpos
        self.o_text.set_pos(self.content_x, self.content_y)

    def set_parent(self, parent):
        self.parent = parent

    def set_w(self, w):
        self.w = w
        self.content_w = self.w-button.border*2-button.margin*2

    def get_content_w(self):
        return self.content_w

    def set_val(self, txt):
        self.txt = txt
        self.o_text.set_val(txt)

    def set_callback(self, callback):
        self.callback = callback

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x+self.w-1 and mouse_y <= self.y+self.h-1:
                if self.callback != None:
                    return self.callback(event)
                else:
                    return False
            else:
                return False
        else:
            return False

class ribbon(i_draw):
    #class static variables goes before __init__
    pad = 1

    border = 1
    border_color = (0, 0, 0)
    margin = 1
    margin_color = (255, 255, 255)

    num_chars = 7
    num_elems = 3

    def __init__(self, h_v=0, num_chars=num_chars,
                              num_elems=num_elems):
        self.parent = None
        self.x = 0
        self.y = 0
        self.h_v = h_v
        self.num_chars = num_chars
        self.num_elems = num_elems

        if self.h_v == 0: #horizontal ribbon
            bw = button.width(self.num_chars)
            bh = button.height()
            self.w = (bw+ribbon.pad)*num_elems+ribbon.border*2+ribbon.margin*2+ribbon.pad #beginning pad
            self.h = bh*1+ribbon.border*2+ribbon.margin*2
        if self.h_v == 1: #vertical ribbon
            bw = button.width(self.num_chars)
            bh = button.height()
            self.h = (bh+ribbon.pad)*num_elems+ribbon.border*2+ribbon.margin*2+ribbon.pad #beginning pad
            self.w = bw*1+ribbon.border*2+ribbon.margin*2

        self.children = []
        self.first_visible = 0 #index to self.children
        self.last_visible = 0 #index to self.children

        if self.h_v == 0: #horizontal ribbon
            self.content_x = self.x+ribbon.border+ribbon.margin+ribbon.pad
            self.content_y = self.y+ribbon.border+ribbon.margin
            self.content_w = self.w-ribbon.border*2-ribbon.margin*2-ribbon.pad
            self.content_h = self.h-ribbon.border*2-ribbon.margin*2
        if self.h_v == 1: #vertical ribbon
            self.content_x = self.x+ribbon.border+ribbon.margin
            self.content_y = self.y+ribbon.border+ribbon.margin+ribbon.pad
            self.content_w = self.w-ribbon.border*2-ribbon.margin*2
            self.content_h = self.h-ribbon.border*2-ribbon.margin*2-ribbon.pad

    def __draw_border(self, surface):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.line(surface, BLACK, (x, y), (x+w-1, y))
        pygame.draw.line(surface, BLACK, (x+w-1, y), (x+w-1, y+h-1))
        pygame.draw.line(surface, BLACK, (x+w-1, y+h-1), (x, y+h-1))
        pygame.draw.line(surface, BLACK, (x, y+h-1), (x, y))

    def __draw_margin(self, surface):
        pass

    def size(self):
        return self.w, self.h

    def set_parent(self, parent):
        self.parent = parent

    def set_w(self, w):
        if self.h_v == 0: #horizontal ribbon
            self.w = w
            self.content_w = self.w-ribbon.border*2-ribbon.margin*2-ribbon.pad

    def set_h(self, h):
        if self.h_v == 1: #vertical ribbon
            self.h = h
            self.content_h = self.h-ribbon.border*2-ribbon.margin*2-ribbon.pad

    def addchild(self, child):
        child_w, child_h = child.size()

        if self.h_v == 0: #horizontal ribbon
            if child_w+ribbon.pad > self.content_w or child_h > self.content_h:
                raise Exception("Error: not able to add this child")
        if self.h_v == 1: #vertical ribbon
            if child_w > self.content_w or child_h+ribbon.pad > self.content_h:
                raise Exception("Error: not able to add this child")

        child.set_parent(self)
        self.children.append(child)
        print("child addedd successfully")

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        if self.h_v == 0: #horizontal ribbon
            self.content_x = self.x+ribbon.border+ribbon.margin+ribbon.pad
            self.content_y = self.y+ribbon.border+ribbon.margin
        if self.h_v == 1: #vertical ribbon
            self.content_x = self.x+ribbon.border+ribbon.margin
            self.content_y = self.y+ribbon.border+ribbon.margin+ribbon.pad

        #setpos of children not needed
        #because first ribbon is placed inside panel
        #and then its children button gets added to it

    #it depends on self.first_visible
    #it sets positions of children and
    #it sets self.last_visible
    def update_children(self):
        start_x = self.content_x
        start_y = self.content_y
        available_w = self.content_w
        available_h = self.content_h

        first = self.first_visible
        num_children = len(self.children)
        #at the least one child is always visible!
        #because all children sizes are lesser than ribbon size
        #so this loop has minimum one iteration
        #so self.last_visible is guaranteed to be set
        for i in range(first, num_children):
            child = self.children[i]
            child_w, child_h = child.size()
            if self.h_v == 0: #horizontal ribbon
                if child_w+ribbon.pad > available_w:
                    break
                else:
                    self.last_visible = i
                    child.set_pos(start_x, start_y)
                    start_x += child_w + ribbon.pad
                    available_w -= child_w + ribbon.pad
            if self.h_v == 1: #vertical ribbon
                if child_h+ribbon.pad > available_h:
                    break
                else:
                    self.last_visible = i
                    child.set_pos(start_x, start_y)
                    start_y += child_h + ribbon.pad
                    available_h -= child_h + ribbon.pad

    def draw(self, surface):
        self.__draw_border(surface)
        self.__draw_margin(surface)
        self.update_children()

        first = self.first_visible
        last = self.last_visible
        for i in range(first, last+1):
            child = self.children[i]
            child.draw(surface)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x+self.w-1 and mouse_y <= self.y+self.h-1:
                if event.button==1 or event.button==3: #1=left, 2=middle, 3=right
                    first = self.first_visible
                    last = self.last_visible
                    for i in range(first, last+1):
                        child = self.children[i]
                        if child.handle_event(event):
                            return True
                    return False
                elif event.button==4 or event.button==5: #4=scrollup, 5=scrolldown
                    if event.button == 4:
                        self.first_visible -= 1
                        #first_visible shouldn't go out of range
                        if self.first_visible == -1:
                            self.first_visible = 0
                        self.update_children()
                    if event.button == 5:
                        self.first_visible += 1
                        #first_visible shouldn't go out of range
                        num_children = len(self.children)
                        if self.first_visible == num_children:
                            self.first_visible = num_children-1
                        #set last_visible and update children positions
                        self.update_children()
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False


class panel(i_draw):
    #class static variables goes before __init__
    pad = 1

    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.children = []
        self.fill_h_v = 1 #0 = fill horizontally
                          #1 = fill vertically

        self.available_x = self.x+panel.pad
        self.available_y = self.y+panel.pad
        self.available_w = self.w-panel.pad #first pad
        self.available_h = self.h-panel.pad #first pad

    def divide_w_wise(self, percentage):
        x1 = self.x
        y1 = self.y
        w1 = round(self.w*percentage/100)
        h1 = self.h
        subpanel1 = panel(x1, y1, w1, h1)
        x2 = self.x + w1
        y2 = self.y
        w2 = self.w - w1
        h2 = self.h
        subpanel2 = panel(x2, y2, w2, h2)
        self.children.append(subpanel1)
        self.children.append(subpanel2)
        #after division no other items
        #can be added to parent panel
        #items can be added only to subpanels
        self.available_w = 0
        self.available_h = 0
        return subpanel1, subpanel2

    def divide_h_wise(self, percentage):
        x1 = self.x
        y1 = self.y
        w1 = self.w
        h1 = round(self.h*percentage/100)
        subpanel1 = panel(x1, y1, w1, h1)
        x2 = self.x
        y2 = self.y + h1
        w2 = self.w
        h2 = self.h - h1
        subpanel2 = panel(x2, y2, w2, h2)
        self.children.append(subpanel1)
        self.children.append(subpanel2)
        #after division no other items
        #can be added to parent panel
        #items can be added only to subpanels
        self.available_w = 0
        self.available_h = 0
        return subpanel1, subpanel2

    def draw(self, surface):
        for child in self.children:
            child.draw(surface)

    def addchild(self, child):
        child_w, child_h = child.size()

        if self.fill_h_v == 1: #fill vertically
            if child_w > self.available_w or child_h+panel.pad > self.available_h:
                raise Exception("Error: no space available to add this child")
            child.set_pos(self.available_x, self.available_y)
            self.available_y += child_h + panel.pad
            self.available_h -= child_h + panel.pad
        if self.fill_h_v == 0: #fill horizontally
            if child_w+panel.pad > self.available_w or child_h > self.available_h:
                raise Exception("Error: no space available to add this child")
            child.set_pos(self.available_x, self.available_y)
            self.available_x += child_w + panel.pad
            self.available_w -= child_w + panel.pad

        child.set_parent(self)
        self.children.append(child)
        print("child addedd successfully")

    def get_available_w(self):
        return self.available_w - panel.pad #last pad

    def get_available_h(self):
        return self.available_h - panel.pad #last pad

    def fill_horizontally(self):
        self.fill_h_v = 0

    def fill_vertically(self):
        self.fill_h_v = 1

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x+self.w-1 and mouse_y <= self.y+self.h-1:
                for child in self.children:
                    if child.handle_event(event):
                        return True
                return False
            else:
                return False
        elif event.type == pygame.KEYDOWN:
            for child in self.children:
                if child.handle_event(event):
                    return True
            return False
        else:
            return False

#this is model of multitext
class multibuf():
    #class static variables goes before __init__
    def __init__(self, vc):
        self.vc = vc

        self.bufs = []
        self.bufs.insert(0, {"count":0, "buf":[None]*100})
        #last '\n' as per posix
        self.bufs[0]["count"] = 1
        buf = self.bufs[0]["buf"]
        buf[0] = '\n'

    def break_into_bufs(self, o_file):
        #pdb.set_trace()
        while True:
            chunk = o_file.read(100)
            if not chunk:
                break

            chunk_len = len(chunk)
            if(chunk_len==100):
                self.bufs.append({"count":100, "buf":list(chunk)})
            else:
                new_buf_dict = {"count":0, "buf":[None]*100}
                new_buf_dict["count"]=chunk_len

                new_buf = new_buf_dict["buf"]
                chunck_as_list = list(chunk)
                new_buf[0:chunk_len] = chunck_as_list[0:chunk_len]

                self.bufs.append(new_buf_dict)

        #insert last '\n' as per posix
        num_bufs = len(self.bufs)
        if num_bufs != 0:
            #check and add last '\n' as per posix
            last_buf_dict = self.bufs[-1]
            last_count = last_buf_dict["count"]
            last_buf = last_buf_dict["buf"]
            if last_count == 100:
                if last_buf[last_count-1] == '\n':
                    pass
                else:
                    new_buf_dict = {"count":0, "buf":[None]*100}
                    new_buf_dict["count"]=1

                    new_buf = new_buf_dict["buf"]
                    new_buf[0] = '\n'

                    self.bufs.append(new_buf_dict)
            else: #last_count < 100
                if last_buf[last_count-1] == '\n':
                    pass
                else:
                    last_buf_dict["count"] = last_count+1
                    last_buf[last_count]='\n'
        else:
            self.bufs.insert(0, {"count":0, "buf":[None]*100})
            #last '\n' as per posix
            self.bufs[0]["count"] = 1
            buf = self.bufs[0]["buf"]
            buf[0] = '\n'

    def set_file(self, filepath):
        self.bufs = []
        o_file = open(filepath, 'r')
        self.break_into_bufs(o_file)
        o_file.close()
        self.vc.notify_on_load()

    def set_str(self, bigbuf):
        self.bufs = []
        o_strio = StringIO(bigbuf)
        self.break_into_bufs(o_strio)
        o_strio.close()
        self.vc.notify_on_load()

    def extend_buf(self, index):
        self.bufs.insert(index+1, {"count":0, "buf":[None]*100})
        src_buf = self.bufs[index]["buf"]
        dst_buf = self.bufs[index+1]["buf"]
        dst_buf[0:50] = src_buf[50:100]
        self.bufs[index]["count"] = 50
        self.bufs[index+1]["count"] = 50

    def find_buf_dict(self, file_offset):
        index=-1
        prev_cumulative_count = 0
        cumulative_count = 0

        num_bufs = len(self.bufs)
        while file_offset >= cumulative_count:
            index = index+1
            if index < num_bufs:
                prev_cumulative_count = cumulative_count
                cumulative_count = prev_cumulative_count+self.bufs[index]["count"]
            else:
                return None, None
        buf_index = index
        buf_offset = file_offset - prev_cumulative_count
        return buf_index, buf_offset

    def ins_char(self, file_offset, char):
        buf_index, buf_offset = self.find_buf_dict(file_offset)
        if buf_index == None and buf_offset == None:
            return

        count = self.bufs[buf_index]["count"]
        buf = self.bufs[buf_index]["buf"]
        if count < 100:
            buf[buf_offset+1:count+1] = buf[buf_offset:count]
            buf[buf_offset] = char
            self.bufs[buf_index]["count"] += 1
        elif count == 100:
            self.extend_buf(buf_index)

            if buf_offset < 50:
                count = 50 #just after extend_buf
                buf = self.bufs[buf_index]["buf"]

                buf[buf_offset+1:count+1] = buf[buf_offset:count]
                buf[buf_offset] = char
                self.bufs[buf_index]["count"] += 1
            else: #>=50
                count = 50 #just after extend_buf
                buf = self.bufs[buf_index+1]["buf"]

                buf_offset = buf_offset - 50
                buf[buf_offset+1:count+1] = buf[buf_offset:count]
                buf[buf_offset] = char
                self.bufs[buf_index+1]["count"] += 1
        else:
            print("Impossible!")
        self.vc.notify_on_ins()

    def del_char(self, file_offset):
        print(file_offset)

        buf_index, buf_offset = self.find_buf_dict(file_offset)
        if buf_index == None and buf_offset == None:
            return

        count = self.bufs[buf_index]["count"]
        buf = self.bufs[buf_index]["buf"]

        if count-1 == 0:
            self.bufs.pop(buf_index)
        else:
            buf[buf_offset:count-1] = buf[buf_offset+1:count]
            buf[count-1]=None
            self.bufs[buf_index]["count"] -= 1

        self.vc.notify_on_del()

    def bksp_char(self, file_offset):
        file_offset -= 1
        print(file_offset)

        #same logic as del_char
        #but notify call is different
        buf_index, buf_offset = self.find_buf_dict(file_offset)
        if buf_index == None and buf_offset == None:
            return

        count = self.bufs[buf_index]["count"]
        buf = self.bufs[buf_index]["buf"]

        if count-1 == 0:
            self.bufs.pop(buf_index)
        else:
            buf[buf_offset:count-1] = buf[buf_offset+1:count]
            buf[count-1]=None
            self.bufs[buf_index]["count"] -= 1

        self.vc.notify_on_bksp()

    def get_a_line(self, file_offset, max_num_chars):
        buf_index, buf_offset = self.find_buf_dict(file_offset)
        if buf_index == None and buf_offset == None:
            return None

        line = []
        num_bufs = len(self.bufs)

        count = self.bufs[buf_index]["count"]
        buf = self.bufs[buf_index]["buf"]
        char = buf[buf_offset]

        while True:
            line.append(char)

            if char == '\n':
                break

            line_len = len(line)
            if line_len == max_num_chars:
                break

            buf_offset += 1

            if buf_offset < count:
                char = buf[buf_offset]
            else:
                buf_offset = 0
                buf_index += 1
                if buf_index < num_bufs:
                    count = self.bufs[buf_index]["count"]
                    buf = self.bufs[buf_index]["buf"]
                    char = buf[buf_offset]
                else:
                    return None
        return line


#this is view controller of multibuf
class multitext(i_draw):
    #class static variables goes before __init__
    pad = 1

    border = 1
    border_color = (0, 0, 0)
    margin = 1
    margin_color = (255, 255, 255)

    num_chars = 7
    num_elems = 3

    def __init__(self, num_chars=num_chars,
                       num_elems=num_elems):
        self.parent = None
        self.num_chars = num_chars
        self.num_elems = num_elems

        self.x = 0
        self.y = 0
        self.w = text.font_w*self.num_chars+multitext.border*2+multitext.margin*2
        self.h = (text.font_h+multitext.pad)*self.num_elems+multitext.border*2+multitext.margin*2+multitext.pad #beginning pad

        self.content_x = self.x+multitext.border+multitext.margin
        self.content_y = self.y+multitext.border+multitext.margin+multitext.pad
        self.content_w = self.w-multitext.border*2-multitext.margin*2
        self.content_h = self.h-multitext.border*2-multitext.margin*2-multitext.pad

        #create children and update their x, y
        self.children = []
        start_x = self.content_x
        start_y = self.content_y
        for i in range(self.num_elems):
            o_text = text()
            o_text.set_parent(self)
            o_text.set_pos(start_x, start_y)
            start_y += text.font_h + multitext.pad
            self.children.append(o_text)
            #o_text.set_val(txt)
            #value strings are set in update_on_load

        #for cursor
        #constants
        self.cursor_w = 1
        self.cursor_h = text.font_h
        #variables
        self.cursor_offset = 0 #independent, similar to file offset
        self.cursor_row = 0 #dependent on cursor_offset
        self.cursor_col = 0 #dependent on cursor_offset
        #actual x, y of cursor is calculated using
        #cursor_row and cursor_col and top_row

        #main data structure of multitext
        self.rows = []
        self.top_row = 0 #adjusted using cursor_row which depends on cursor_offset

        #initialize model
        self.mbuf = multibuf(self)
        self.mbuf.set_str("") #this adds default '\n' as per posix
        #update_on_load is called
        #update_on_load recreates self.rows
        #update_on_load sets value strings of self.children


    def __draw_border(self, surface):
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        pygame.draw.line(surface, BLACK, (x, y), (x+w-1, y))
        pygame.draw.line(surface, BLACK, (x+w-1, y), (x+w-1, y+h-1))
        pygame.draw.line(surface, BLACK, (x+w-1, y+h-1), (x, y+h-1))
        pygame.draw.line(surface, BLACK, (x, y+h-1), (x, y))

    def __draw_margin(self, surface):
        pass

    def size(self):
        return self.w, self.h

    def set_parent(self, parent):
        self.parent = parent

    def set_w(self, w):
        self.w = w
        self.content_w = self.w-multitext.border*2-multitext.margin*2
        self.num_chars = self.content_w // text.font_w
        #no need to recreate children
        #no need to update their x, y
        #but we need to update children value strings
        #because self.num_chars got new value
        self.update_on_load() #depends on self.num_chars

    def set_h(self, h):
        self.h = h
        self.content_h = self.h-multitext.border*2-multitext.margin*2-multitext.pad
        self.num_elems = self.content_h // (text.font_h + multitext.pad)
        #recreate children and update their x, y
        #because now we have more space for more lines
        self.children = []
        start_x = self.content_x
        start_y = self.content_y
        for i in range(self.num_elems):
            o_text = text()
            o_text.set_parent(self)
            o_text.set_pos(start_x, start_y)
            start_y += text.font_h + multitext.pad
            self.children.append(o_text)
            #o_text.set_val(txt)
            #value strings are set in update_on_load
        self.update_on_load() #depends on self.num_chars

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.content_x = self.x+multitext.border+multitext.margin
        self.content_y = self.y+multitext.border+multitext.margin+multitext.pad
        #only update children x, y
        #no need of recreating children
        #no need of setting their values
        start_x = self.content_x
        start_y = self.content_y
        for o_text in self.children:
            o_text.set_pos(start_x, start_y)
            start_y += text.font_h + multitext.pad
            #o_text.set_val(txt)
            #value already set in __init__(), set_w(), set_h()

    #used by children to draw text
    def get_content_w(self):
        return self.content_w

    #this is for initializing multitext
    def set_file(self, filepath):
        self.mbuf.set_file(filepath)
        #update_on_load is called

    #this is for initializing multitext
    def set_str(self, bigbuf):
        self.mbuf.set_str(bigbuf)
        #update_on_load is called

    #this uses self.cursor_offset
    #to set self.cursor_row and self.cursor_col
    def calc_cursor_row_col(self):
        index=-1
        prev_cumulative_count = 0
        cumulative_count = 0

        num_rows = len(self.rows)
        while self.cursor_offset >= cumulative_count:
            index = index+1
            if index < num_rows:
                prev_cumulative_count = cumulative_count
                cumulative_count = prev_cumulative_count+self.rows[index]["length"]
            else:
                return None, None
        self.cursor_row = index
        self.cursor_col = self.cursor_offset - prev_cumulative_count

    def move_cursor_right(self):
        #do not move right of last character of last row which is '\n'
        num_rows = len(self.rows)
        line_len = self.rows[num_rows-1]["length"]
        last_offset = self.rows[num_rows-1]["offset"] + line_len-1
        if self.cursor_offset == last_offset:
            return
        self.cursor_offset += 1
        self.calc_cursor_row_col()
        #adjust top_row
        if self.cursor_row > self.top_row+self.num_elems-1:
            self.top_row += 1

    def move_cursor_left(self):
        #do not move left when cursor at offset 0
        if self.cursor_offset == 0:
            return
        self.cursor_offset -= 1
        self.calc_cursor_row_col()
        #adjust top_row
        if self.cursor_row < self.top_row:
            self.top_row -= 1

    def move_cursor_up(self):
        if self.cursor_row == 0:
            return
        self.cursor_row -= 1
        self.cursor_col = 0
        self.cursor_offset = self.rows[self.cursor_row]["offset"] + self.cursor_col
        #adjust top_row
        if self.cursor_row < self.top_row:
            self.top_row -= 1

    def move_cursor_down(self):
        num_rows = len(self.rows)
        if self.cursor_row == num_rows - 1:
            return
        self.cursor_row += 1
        self.cursor_col = 0
        self.cursor_offset = self.rows[self.cursor_row]["offset"] + self.cursor_col
        #adjust top_row
        if self.cursor_row > self.top_row+self.num_elems-1:
            self.top_row += 1

    #important notes:
    #mbuf.ins_char(), mbuf.del_char() and mbuf.bksp_char()
    #is guaranteed to work as long as file offset is correct.
    #it is the responsibility of multitext functions
    #insert_char(), delete_char() or backspace_char()
    #to see if user is allowed to do so.
    #that is why multibuf functions are guaranteed to work.
    #and after they finish work, they modify mbuf.bufs[].
    #either 1 char is added or 1 char is removed.
    #this leaves mbuf.bufs[] in a new changed state.
    #but, cursor state of multitext remains in old state!
    #now the interesting thing happens. multibuf calls
    #notify_on_ins() or notify_on_del() or notify_on_bksp().
    #these in turn calls update_on_ins(), update_on_del()
    #and update_on_bksp(). when we are inside these calls,
    #we must remember that cursor_offset, cursor_row,
    #cursor_col as well as rows[], all are in old state!
    #that is why we must be careful inside update functions.
    #we only changed rows[] data structure to new state
    #inside these update functions, and we call (as needed)
    #move_cursor_right() or move_cursor_right() to change
    #cursor_offset, cursor_row and cursor_col to new state,
    #as well as to change top_row to new state!

    def insert_char(self, char):
        self.mbuf.ins_char(self.cursor_offset, char)
        self.move_cursor_right() #precondition of move_cursor_right() will satisfy after a char is inserted

    def delete_char(self):
        #do not delete last character of last row which is '\n'
        num_rows = len(self.rows)
        line_len = self.rows[num_rows-1]["length"]
        last_offset = self.rows[num_rows-1]["offset"] + line_len-1
        if self.cursor_offset == last_offset:
            return
        self.mbuf.del_char(self.cursor_offset)
        #no need of cursor update

    def backspace_char(self):
        #do not backspace when cursor at offset 0
        if self.cursor_offset == 0:
            return
        self.mbuf.bksp_char(self.cursor_offset)
        self.move_cursor_left()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = event.pos
            if mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x+self.w-1 and mouse_y <= self.y+self.h-1:
                if event.button==1 or event.button==3: #1=left, 2=middle, 3=right
                    return self.handle_click(event)
                else:
                    return False
            else:
                return False
        elif event.type == pygame.KEYDOWN:
            return self.handle_key(event)
        else:
            return False

    def handle_click(self, event):
        #pdb.set_trace()
        mouse_x, mouse_y = event.pos

        #mouse pos wrt multitext
        mouse_x -= self.content_x
        mouse_y -= self.content_y

        #cur_row and cur_col are not index to rows[]
        cur_row = mouse_y // (text.font_h + multitext.pad)
        cur_col = mouse_x // (text.font_w)

        #keep cursor to visible lines
        num_total_rows = len(self.rows)
        num_visible_rows = num_total_rows - self.top_row
        #num_visible_rows should never be more than self.num_elems
        if num_visible_rows > self.num_elems:
            num_visible_rows = self.num_elems
        #> for case when num_visible_rows is less than self.num_elems
        #= for case when we have some space after self.num_elems lines
        if cur_row >= num_visible_rows:
            cur_row = num_visible_rows-1 #cursor_row is 0 based

        #keep cursor to visible characters
        #cursor should always be left to every characters
        num_chars_in_cursor_row = self.rows[self.top_row + cur_row]["length"]
        #> for case when num_chars_in_cursor_row is less than self.num_chars
        #= for case when we have some space after self.num_chars characters
        if cur_col >= num_chars_in_cursor_row:
            cur_col = num_chars_in_cursor_row-1 #cursor_col is 0 based

        self.cursor_row = self.top_row + cur_row
        self.cursor_col = cur_col
        self.cursor_offset = self.rows[self.cursor_row]["offset"] + self.cursor_col
        #self.top_row remains unaltered

    def handle_key(self, event):
        print("mt key")
        if event.key in range(32,127):
            src = r"`1234567890-=qwertyuiop[]\asdfghjkl;\'zxcvbnm,./"
            dest = r'~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:\"ZXCVBNM<>?'
            ch = chr(event.key)
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_RSHIFT] or pressed[pygame.K_LSHIFT] and ch in src:
                ch = dest[src.index(ch)]
            print(ch)
            self.insert_char(ch)

        elif event.key == pygame.K_BACKSPACE:
            print("backspace")
            self.backspace_char()

        elif event.key == pygame.K_DELETE:
            print("delete")
            self.delete_char()

        elif event.key == pygame.K_RETURN:
            print("enter")
            self.insert_char('\n')

        elif event.key == pygame.K_LEFT:
            self.move_cursor_left()

        elif event.key == pygame.K_RIGHT:
            self.move_cursor_right()

        elif event.key == pygame.K_UP:
            self.move_cursor_up()

        elif event.key == pygame.K_DOWN:
            self.move_cursor_down()

        else:
            print("key not supported")

    def list_to_str(self, l):
        new_str = ""
        for c in l:
            #if c != '\n':
                #new_str += c
            new_str += c
        return new_str

    #this depends on self.num_chars
    def load_rows(self):
        self.rows = []
        file_offset = 0
        while True:
            line = self.mbuf.get_a_line(file_offset, self.num_chars)
            if not line:
                break

            line_len = len(line)
            new_row_dict = {"offset":file_offset, "length":line_len, "newline":False}
            if line[-1] == '\n':
                new_row_dict["newline"]=True
            self.rows.append(new_row_dict)

            file_offset += line_len

    #this depends on self.num_chars
    def gen_rows(self):
        rows = []
        file_offset = 0
        while True:
            line = self.mbuf.get_a_line(file_offset, self.num_chars)
            if not line:
                break

            line_len = len(line)
            new_row_dict = {"offset":file_offset, "length":line_len, "newline":False}
            if line[-1] == '\n':
                new_row_dict["newline"]=True
            rows.append(new_row_dict)

            file_offset += line_len

        return rows

    #this depends on self.num_chars
    def get_updated_rows(self, start_offset, end_offset):
        partial_rows = []
        file_offset = start_offset
        while True:
            if file_offset == end_offset: #end_offset is excluding offset
                break

            line = self.mbuf.get_a_line(file_offset, self.num_chars)
            if not line:
                print("impossible!") #because of above guard
                break

            line_len = len(line)
            new_row_dict = {"offset":file_offset, "length":line_len, "newline":False}
            if line[-1] == '\n':
                new_row_dict["newline"]=True
            partial_rows.append(new_row_dict)

            file_offset += line_len

        return partial_rows

    #this depends on self.top_row
    def update_children_values(self):
        row_index = self.top_row
        num_total_rows = len(self.rows)
        for o_text in self.children:
            if row_index < num_total_rows:
                file_offset = self.rows[row_index]["offset"]
                line = self.mbuf.get_a_line(file_offset, self.num_chars)
                txt = self.list_to_str(line)
                #print(txt)
                o_text.set_val(txt)

                row_index += 1
            else:
                o_text.set_val("")

    def notify_on_load(self):
        self.update_on_load()

    def update_on_load(self):
        self.load_rows()

    def notify_on_ins(self):
        self.update_on_ins()

    def notify_on_del(self):
        self.update_on_del()

    def notify_on_bksp(self):
        self.update_on_bksp()

    #for performance improvement
    def update_on_ins(self):
        #save index to insert updated rows into rows[] later
        rows_ins_idx = self.cursor_row

        #from this offset we need to update rows
        #so save start offset
        start_off = self.rows[self.cursor_row]["offset"]

        #index to delete rows from rows[] for updation
        rows_del_idx = self.cursor_row

        #delete all partial rows without newline
        while True:
            if self.rows[rows_del_idx]["newline"]==False:
                self.rows.pop(rows_del_idx)
            else:
                break

        #before deleting ultimate partial row with newline
        #save end offset, because we may be at last row!
        end_off = self.rows[rows_del_idx]["offset"]
        end_off += self.rows[rows_del_idx]["length"] #this is excluding offset
        end_off += 1 #since insert has added one character to mbuf.bufs[], next row offset must be 1 greater

        #delete the ultimate partial row with newline
        self.rows.pop(rows_del_idx)

        #get newly updated rows
        partial_rows = self.get_updated_rows(start_off, end_off)

        #insert them into rows[]
        while partial_rows:
            self.rows.insert(rows_ins_idx, partial_rows[0])
            rows_ins_idx += 1
            partial_rows.pop(0)

        #change offset of rest of the rows
        num_rows = len(self.rows)
        while True:
            if rows_ins_idx == num_rows:
                break
            self.rows[rows_ins_idx]["offset"] += 1 #because of insert
            rows_ins_idx += 1



        #test by compare
        orig_rows = self.gen_rows()
        orig_num_rows = len(orig_rows)
        edit_num_rows = len(self.rows)
        if orig_num_rows != edit_num_rows:
            print("Error: len not equal")
        idx = 0
        while True:
            if idx == orig_num_rows:
                break
            if orig_rows[idx]["offset"] != self.rows[idx]["offset"]:
                print("Error: offset not equal")
            if orig_rows[idx]["length"] != self.rows[idx]["length"]:
                print("Error: length not equal")
            if orig_rows[idx]["newline"] != self.rows[idx]["newline"]:
                print("Error: newline not equal")
            idx += 1

    #for performance improvement
    def update_on_del(self):
        num_rows = len(self.rows)

        #save index to insert updated rows into rows[] later
        rows_ins_idx = self.cursor_row

        #from this offset we need to update rows
        #so save start offset
        start_off = self.rows[self.cursor_row]["offset"]

        #index to delete rows from rows[] for updation
        rows_del_idx = self.cursor_row

        #if current row is last row
        if rows_del_idx == num_rows-1:
            #before deleting ultimate partial row with newline
            #save end offset, because we may be at last row!
            end_off = self.rows[rows_del_idx]["offset"]
            end_off += self.rows[rows_del_idx]["length"] #this is excluding offset
            end_off -= 1 #since delete has removed one character from mbuf.bufs[], next row offset must be 1 lesser

            #delete the ultimate partial row with newline
            self.rows.pop(rows_del_idx)

        #if not last row
        else:
            #if current row ending with newline
            if self.rows[rows_del_idx]["newline"]==True:
                #first delete this partial row with newline
                self.rows.pop(rows_del_idx)
            #after this, also delete next line coming after current row
            #because delete might have deleted the newline character

            #if current row not ending with newline
            #then only below code

            #delete all partial rows without newline
            while True:
                if self.rows[rows_del_idx]["newline"]==False:
                    self.rows.pop(rows_del_idx)
                else:
                    break

            #before deleting ultimate partial row with newline
            #save end offset, because we may be at last row!
            end_off = self.rows[rows_del_idx]["offset"]
            end_off += self.rows[rows_del_idx]["length"] #this is excluding offset
            end_off -= 1 #since delete has removed one character from mbuf.bufs[], next row offset must be 1 lesser

            #delete the ultimate partial row with newline
            self.rows.pop(rows_del_idx)

        #get newly updated rows
        partial_rows = self.get_updated_rows(start_off, end_off)

        #insert them into rows[]
        while partial_rows:
            self.rows.insert(rows_ins_idx, partial_rows[0])
            rows_ins_idx += 1
            partial_rows.pop(0)

        #change offset of rest of the rows
        num_rows = len(self.rows)
        while True:
            if rows_ins_idx == num_rows:
                break
            self.rows[rows_ins_idx]["offset"] -= 1 #because of delete
            rows_ins_idx += 1



        #test by compare
        orig_rows = self.gen_rows()
        orig_num_rows = len(orig_rows)
        edit_num_rows = len(self.rows)
        if orig_num_rows != edit_num_rows:
            print("Error: len not equal")
        idx = 0
        while True:
            if idx == orig_num_rows:
                break
            if orig_rows[idx]["offset"] != self.rows[idx]["offset"]:
                print("Error: offset not equal")
            if orig_rows[idx]["length"] != self.rows[idx]["length"]:
                print("Error: length not equal")
            if orig_rows[idx]["newline"] != self.rows[idx]["newline"]:
                print("Error: newline not equal")
            idx += 1

    #for performance improvement
    def update_on_bksp(self):
        num_rows = len(self.rows)

        #if cursor not at zero, it behaves as update_on_ins
        if self.cursor_col != 0:

            #save index to insert updated rows into rows[] later
            rows_ins_idx = self.cursor_row

            #from this offset we need to update rows
            #so save start offset
            start_off = self.rows[self.cursor_row]["offset"]

            #index to delete rows from rows[] for updation
            rows_del_idx = self.cursor_row

            #delete all partial rows without newline
            while True:
                if self.rows[rows_del_idx]["newline"]==False:
                    self.rows.pop(rows_del_idx)
                else:
                    break

            #before deleting ultimate partial row with newline
            #save end offset, because we may be at last row!
            end_off = self.rows[rows_del_idx]["offset"]
            end_off += self.rows[rows_del_idx]["length"] #this is excluding offset
            end_off -= 1 #since backspace has removed one character from mbuf.bufs[], next row offset must be 1 lesser

            #delete the ultimate partial row with newline
            self.rows.pop(rows_del_idx)

        #if cursor is at zero, it behaves as update_on_del
        else:
            #note that even if cursor_col == 0, cursor_row can not be 0 here
            #because in that case backspace wouldn't have been possible even

            #save index to insert updated rows into rows[] later
            rows_ins_idx = self.cursor_row-1

            #from this offset we need to update rows
            #so save start offset
            start_off = self.rows[self.cursor_row-1]["offset"]

            #index to delete rows from rows[] for updation
            rows_del_idx = self.cursor_row-1

            #if current row ending with newline
            if self.rows[rows_del_idx]["newline"]==True:
                #first delete this partial row with newline
                self.rows.pop(rows_del_idx)
            #after this, also delete next line coming after current row
            #because backspace might have deleted the newline character

            #if current row not ending with newline
            #then only below code

            #delete all partial rows without newline
            while True:
                if self.rows[rows_del_idx]["newline"]==False:
                    self.rows.pop(rows_del_idx)
                else:
                    break

            #before deleting ultimate partial row with newline
            #save end offset, because we may be at last row!
            end_off = self.rows[rows_del_idx]["offset"]
            end_off += self.rows[rows_del_idx]["length"] #this is excluding offset
            end_off -= 1 #since backspace has removed one character from mbuf.bufs[], next row offset must be 1 lesser

            #delete the ultimate partial row with newline
            self.rows.pop(rows_del_idx)


        #get newly updated rows
        partial_rows = self.get_updated_rows(start_off, end_off)

        #insert them into rows[]
        while partial_rows:
            self.rows.insert(rows_ins_idx, partial_rows[0])
            rows_ins_idx += 1
            partial_rows.pop(0)

        #change offset of rest of the rows
        num_rows = len(self.rows)
        while True:
            if rows_ins_idx == num_rows:
                break
            self.rows[rows_ins_idx]["offset"] -= 1 #because of backspace
            rows_ins_idx += 1



        #test by compare
        orig_rows = self.gen_rows()
        orig_num_rows = len(orig_rows)
        edit_num_rows = len(self.rows)
        if orig_num_rows != edit_num_rows:
            print("Error: len not equal")
        idx = 0
        while True:
            if idx == orig_num_rows:
                break
            if orig_rows[idx]["offset"] != self.rows[idx]["offset"]:
                print("Error: offset not equal")
            if orig_rows[idx]["length"] != self.rows[idx]["length"]:
                print("Error: length not equal")
            if orig_rows[idx]["newline"] != self.rows[idx]["newline"]:
                print("Error: newline not equal")
            idx += 1


    def __draw_cursor(self, surface):
        x = self.content_x + (text.font_w)*self.cursor_col
        y = self.content_y + (text.font_h + multitext.pad)*(self.cursor_row - self.top_row)

        pygame.draw.line(surface, RED, (x, y), (x, y+text.font_h-1))

    def draw(self, surface):
        self.__draw_border(surface)
        self.__draw_margin(surface)
        self.update_children_values()
        for child in self.children:
            child.draw(surface)
        self.__draw_cursor(surface)

# 2 - Define constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 10

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()
#this is to generate repeated key down events on "key press and hold"
#first param is delay after first key down event
#second param is interval after second key down event onwards
pygame.key.set_repeat(400,100)

# 4 - Load assets: image(s), sound(s),  etc.

# 5 - Initialize variables
pan = panel(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
l_pan, r_pan = pan.divide_w_wise(65)
lt_pan, lb_pan = l_pan.divide_h_wise(70)

a_btn = button()
pw = lt_pan.get_available_w()
#print(pw)
a_btn.set_w(pw)
lt_pan.addchild(a_btn)
a_btn.set_val("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

a_rbn = ribbon()
pw = lt_pan.get_available_w()
#print(pw)
a_rbn.set_w(pw)
lt_pan.addchild(a_rbn)
d_btn = button()
a_rbn.addchild(d_btn)
e_btn = button()
a_rbn.addchild(e_btn)
f_btn = button()
a_rbn.addchild(f_btn)
g_btn = button()
a_rbn.addchild(g_btn)
h_btn = button()
a_rbn.addchild(h_btn)
i_btn = button()
a_rbn.addchild(i_btn)
j_btn = button()
a_rbn.addchild(j_btn)
k_btn = button()
a_rbn.addchild(k_btn)
l_btn = button()
a_rbn.addchild(l_btn)
d_btn.set_val("Mani..d")
e_btn.set_val("Mani..e")
f_btn.set_val("Mani..f")
g_btn.set_val("Mani..g")
h_btn.set_val("Mani..h")
i_btn.set_val("Mani..i")
j_btn.set_val("Mani..j")
k_btn.set_val("Mani..k")
l_btn.set_val("Mani..l")
def dcallback(event):
    print("dcallback")
def ecallback(event):
    print("ecallback")
def fcallback(event):
    print("fcallback")
def gcallback(event):
    print("gcallback")
def hcallback(event):
    print("hcallback")
def icallback(event):
    print("icallback")
def jcallback(event):
    print("jcallback")
def kcallback(event):
    print("kcallback")
def lcallback(event):
    print("lcallback")
d_btn.set_callback(dcallback)
e_btn.set_callback(ecallback)
f_btn.set_callback(fcallback)
g_btn.set_callback(gcallback)
h_btn.set_callback(hcallback)
i_btn.set_callback(icallback)
j_btn.set_callback(jcallback)
k_btn.set_callback(kcallback)
l_btn.set_callback(lcallback)

a_mt = multitext()
pw = lt_pan.get_available_w()
ph = lt_pan.get_available_h()
a_mt.set_w(pw)
a_mt.set_h(ph)
lt_pan.addchild(a_mt)
a_mt.set_str("The Mother. Sri Aurobindo. My prayer at the lotus feet of her.\nThe Mother. Sri Aurobindo.\nMy prayer at the lotus feet of her. The Mother.\nSri Aurobindo. My prayer at the lotus feet of her.\nThe Mother. Sri Aurobindo. My prayer\nat the lotus feet of her. The\nMother. Sri Aurobindo. My prayer at\nthe lotus feet of her.\n\n")
#a_mt.set_str(' !\"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~')
#a_mt.set_str("")
#a_mt.set_file("a.py")

b_btn = button()
pw = lb_pan.get_available_w()
#print(pw)
b_btn.set_w(pw)
lb_pan.addchild(b_btn)
b_btn.set_val("abcdefghijklmnopqrstuvwxyz")


c_btn = button()
pw = r_pan.get_available_w()
#print(pw)
c_btn.set_w(pw)
r_pan.addchild(c_btn)
c_btn.set_val("0123456789")


# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Clicked the close button? Quit pygame and end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYDOWN:
            pan.handle_event(event)

    # 8  Do any "per frame" actions


    # 9 - Clear the window
    window.fill(WHITE)

    # 10 - Draw all window elements
    pan.draw(window)

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait
