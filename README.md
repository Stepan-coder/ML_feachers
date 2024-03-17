## Предистория

Уже несколько лет наша команда активно участвует в хакатонах и демонстрирует высокие результаты, занимая призовые места. В процессе участия я, в свою очередь, специализируюсь в области машинного обучения и анализа данных, представляя команду в роли специалиста по ML / Data Science.

Однако, на протяжении многих хакатонов я столкнулся с повторяющейся необходимостью писать однотипные операции и функции для обработки данных с использованием библиотеки pandas. Это занимало значительное количество времени на написание самого кода, а что самое обидное - на его отладку.

Именно из-за этой рутины у меня зародилась идея создания пет-проекта на Python - некой «надстройки» над pandas и numpy. Моя цель заключается в том, чтобы с помощью простых и эффективных функций упростить выполнение сложных операций над данными, таких как объединение датафреймов, автоматическое определение типов столбцов, автоматический анализ статистики как по всему датасету, так и по отдельным столбцам, и многие другие функции.

Такой подход позволи не только мне, но и всей команде значительно ускорить процесс работы над проектами в области машинного обучения. Благодаря этой  «надстройке», у нас остается больше времени для более глубокое изучение и понимание данных, а так же на реализацию самих моделей, что в рамках хакатона позволяет значительно вырываться вперед. [TenderHack Казань первое место](https://tenderhack.ru/samara), [TenderHack Пермь первое место](https://tenderhack.ru/perm)

## Что сделано?

Разумеется, на данный момент код значительно устарел, т.к. он писался непосредственно на хакатонах, что соответственно порой вызывает вопросу к его качеству и оптимизации. Так же на момент его «первичного» создания, порядка 4-5 лет назад ~~(на GitHub он был выложен по причине необходимости его использования на хостинге, до этого, код лежал «в папке» на рабочем столе _[в тот момент я не очень понимал зачем нужен гит, да и разрабатывал я его в одиночку]_)~~. Но он уже обладает функционалом «менеджера» DataFrame’ов позволяя «жонглировать» ими, т.е. получать с них данные «синхронно» ~~разумеется, это уже реализовано в большинстве СУБД, но именно с pandas так никто не «развлекался»~~. Умеет их по разному мержить и джоинить, позволяет высчитывать статистически важные показатели и проводить автоматическую предобработку данных, высчитывая «выбросы» и фильтруя по заданным правилам. 

## Что плани(~~ровалось~~)руется

Разумеется, необходимо привести код к S.O.L.I.D., т.к. даже на тот момент у меня уже было ощущение, что я явно делаю «что то не так». 

Так же коду требуется значительная оптимизация, т.к. на одном из хакатонов организаторы выгрузили 100 млн строк данных (~30 ГБ) и модуль показал себя с не самой хорошей стороны «зависнув» на 3 часа драгоценного времени _(слава богу отработал нормально, заняли тогда 4 место :+1:)_. 

Ещё одним интересным решением, как мне тогда казалось создание «менеджера моделей sklearn» для автоматического подбора гиперпараметров, чтобы можно было быстро и автоматически  протестировать модели и «оставить» самую лучшую(крайне полезная штука на маленьких хакатонах по 10-30 тыс., не много конечно, но приятно). 

В последствии, моим сокомандником была предложена ещё одна идея - добавить к этому всему API изахостить на каком-нибудь мощном хостинге, чтобы вычисления происходили на удаленной машине.
