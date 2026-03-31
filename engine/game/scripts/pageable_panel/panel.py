from game.scripts.pageable_panel.page import Page

class Panel:
    def __init__(self, pages:list[Page]=[]):
        self.current_page_index = 0
        self.pages = pages

    def get_current_page(self):
        return self.get_page(self.current_page_index) # I AM SO FKING DUMD IVE BEEN DEBUGGIN THIS FOR 30 MINS AND I JUST FORGOT THE return ::::(((

    def get_page(self, pageIndex:int):
        if self.pages != []:
            if pageIndex in range(len(self.pages)):
                return self.pages[pageIndex]
            else:
                print("mod page getter fail")
                return None
        else:
            print("mod page getter fail - no pages")
            return None
            
    def get_pages(self):
        return self.pages
            
    def add_page(self, pageToAdd:Page):
        self.pages.append(pageToAdd)

    def set_pages(self, pages:list[Page]):
        self.pages = pages
        self.current_page_index = 0 # safety reset?

    def clear_pages(self):
        self.set_pages([])

    def next_page(self):
        if self.pages != None:
            self.current_page_index += 1

            if self.current_page_index > len(self.pages) - 1:
                self.current_page_index = 0

    def prev_page(self):
        if self.pages != None:
            self.current_page_index -= 1

            if self.current_page_index < 0:
                self.current_page_index = len(self.pages) - 1