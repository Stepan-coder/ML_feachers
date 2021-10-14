from RA.Manager.Manager import *
from RA.DataSet.DataSet import *


warnings.filterwarnings("ignore")

manager = Manager(path=os.getcwd(), project_name="test_project")
manager.create_DataSet(dataset_name="table")
manager.DataSet("table").load_excel_dataset(excel_file="skladskoy-uchet.xlsx",
                                            sheet_name="Поставщики")
print(manager.DataSet("table").get_column_statinfo(column_name="Поставщики", extended=True).get_min_value())


# print(manager.DataSet("Original DataSet").get_column_statinfo(column_name="A", extended=True).get_letters_distribution())
#
# print(manager.DataSet("Original DataSet"))


# Надо разделить классы колон! Тип пусть у флоатов будут свои методы и свой функционал, у строк - другой, у булев - третий

# Исходя из личного опыта, стало понятно, что задачи всегда разные и что создать платформу с автообучением
# сложно и что в принципе такие уже есть. Печально. НО
# Можно сделать платформу для начинающих датасантистов! Предоставляем услуги, по обработке и визуализыции данных
# Т.е. Чел грузит свой датасет к нам, и с помощью простых кнопок его редактирует (перетаскивает колонки, группирует,
# смотрит что за данные)
# УСКОРЯЕТ РАБОТУ ПО ОЧИСТКЕ И ФИЛЬТРАЦИИ ДАТАСЕТА
# Нужно создать аккаунт на патреоне и пусть туда люди донатят (на развитие проекта), в последствии туда может
# подключиться и бизнес, потому что это удобнее, чем exel
