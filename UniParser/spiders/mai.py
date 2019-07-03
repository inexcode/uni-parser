import scrapy


class MaiSpider(scrapy.Spider):
    name = 'MAI'

    start_urls = ['https://mai.ru/priem/list/']

    def parse(self, response):
        for place in response.css('select#place option'):
            if place.attrib['value'] != 0:
                yield response.follow('https://mai.ru/priem/list/data2/' + place.attrib['value'] + '.html', self.parse_place)

    def parse_place(self, response):
        for level in response.css('option'):
            if level.attrib['value'] != 0:
                yield response.follow('https://mai.ru/priem/list/data2/' + level.attrib['value'] + '.html', self.parse_level)

    def parse_level(self, response):
        for course in response.css('option'):
            if course.attrib['value'] != 0:
                yield response.follow('https://mai.ru/priem/list/data2/' + course.attrib['value'] + '.html', self.parse_course)

    def parse_course(self, response):
        for form in response.css('option'):
            if form.attrib['value'] != 0:
                yield response.follow('https://mai.ru/priem/list/data2/' + form.attrib['value'] + '.html', self.parse_form)

    def parse_form(self, response):
        for base in response.css('option'):
            if base.attrib['value'] != 0:
                yield response.follow('https://mai.ru/priem/list/data2/' + base.attrib['value'] + '.html', self.parse_table)

    def parse_table(self, response):

        filial = response.url[48]
        if filial == '1':
            filial = 'МАИ'
        elif filial == '2':
            filial = 'Филиал "Восход" МАИ'
        elif filial == '3':
            filial = 'Филиал "Стрела МАИ"'
        elif filial == '4':
            filial = 'Ступинский филиал МАИ'
        elif filial == '5':
            filial = 'Филиал "Взлет МАИ"'
        else:
            filial = 'Error'


        course_fancy = response.css('p b::text')[0].get()
        course_code = course_fancy[:8]
        course_fancy = course_fancy[8:].strip()

        for table in response.css('.data-table'):
            for person in table.css('tr'):
                if person.css('td::text'):
                    try:
                        name = person.css('td::text')[1].getall()[0]
                        case = person.css('td::text')[2].getall()[0]
                        exam = person.css('td::text')[3].getall()[0]

                        yield {
                            'filial': filial,
                            'course_code': course_code,
                            'course_name': course_fancy,
                            'name': name,
                            'case': case,
                            'exam_type': exam,
                        }
                    except Exception as e:
                        print(e)
                        pass
                
                
