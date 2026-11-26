# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `a890f71d` · 9/9 posts written · **6/9 passed every check** · 40 Claude calls · $0.54 ($0.060 per post)

| Check | Pass rate |
| --- | --- |
| facts | 100% |
| glossary | 100% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 89% |
| reviewer | 100% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 3.89 |
| language | 4.00 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/5 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | 3/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/3 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |

## Details

### min-wage-mb

**У Манітобі мінімальну зарплату підвищать до 16,50 долара за годину**

Від 1 жовтня мінімальна погодинна оплата праці в Манітобі становитиме 16,50 долара. Про це в уряді провінції повідомили у вівторок. Підвищення — 65 центів на годину.

Розмір мінімальної зарплати прив'язаний до інфляції в провінції: так вимагає закон, ухвалений 2023 року. За словами міністра праці Деніела Моро (Daniel Moreau), мінімальну ставку отримують близько 40 тисяч працівників, здебільшого в роздрібній торгівлі та закладах харчування. Роботодавці мають платити за новою ставкою за всі години, відпрацьовані від 1 жовтня, зокрема студентам і працівникам на неповну зайнятість. Ставка в Манітобі залишиться нижчою, ніж у Британській Колумбії, але вищою, ніж у Саскачевані.

Торгово-промислова палата Манітоби (Manitoba Chambers of Commerce) зазначила, що малий бізнес візьме додаткові витрати на себе, але просить у наступні роки повідомляти про зміни заздалегідь. За словами представників палати, багато її членів і так платять вище мінімальної ставки, щоб залучити персонал.

Judge: Accuracy: facts and numbers match the source. Minor omission: Moreau's quote about groceries and rent is left out, and the Winnipeg news conference is not mentioned. "Manitoba Chambers of Commerce" is rendered as "Торгово-промислова палата Манітоби", which is a slight liberty because it is really a network of chambers, and a rendering like "Торговельні палати Манітоби" would fit better. Language: mostly natural. "Торгово-промислова" should be "торговельно-промислова". "Візьме додаткові витрати на себе" is slightly clumsy, and "візьме на себе додаткові витрати" is better. "Від 1 жовтня" is fine, but "з 1 жовтня" is more standard. "Працівникам на неповну зайнятість" is a bit stilted, and "працівникам, що працюють неповний день" would be more natural. "Повідомили в уряді" is fine. Usefulness: clear and concise. It does not explain why this matters to readers, such as workers or employers in the Ukrainian community, and the key point about all hours worked from Oct 1 is buried in the middle of a paragraph.

### rcmp-deepfake

**Шахраї з дипфейками виманили в мешканців Метро-Ванкувера 2,3 млн доларів**

Канадська королівська кінна поліція (RCMP) попереджає мешканців агломерації Метро-Ванкувер про романтичні шахрайства, у яких зловмисники видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

Цього року про втрати повідомили 85 людей, а загальна сума сягає 2,3 млн доларів. Здебільшого шахраї знайомилися з жертвами в застосунках для знайомств або в соцмережах. Потім вони проводили короткі відеодзвінки, під час яких обличчя й голос підміняв дипфейк, і через це вигадана особа здавалася переконливою. Коли довіра з'являлася, починалися прохання про гроші: нібито на лікування, через заблокований банківський рахунок або для вигідного вкладення.

«Дзвінки виглядають справжніми, і саме тому такі шахрайства так ефективно діють», — наголосила сержантка Пріая Сандху (Priya Sandhu) з відділу фінансових злочинів RCMP у Саррі.

Поліція радить насторожитися, якщо співрозмовник не може зустрітися наживо, різко обриває дзвінок, коли його просять повернути голову, або вимагає криптовалюту чи подарункові картки. Якщо ви вже переказали гроші, негайно зв'яжіться з банком, а потім повідомте місцеву поліцію та Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: the name Priya is rendered "Пріая", which is an odd transliteration (should be "Пріа" or "Прія"). "а потім повідомте поліцію" adds an order of steps that the source does not specify. The headline "виманили" states the losses as proven fact, whereas the source says victims "reported losing". Language: "і через це вигадана особа здавалася переконливою" is a bit clunky. "ефективно діють" is slightly awkward. "Коли довіра з'являлася" is acceptable but could be smoother. Otherwise the text is natural and the glossary name is used correctly. Usefulness: clear, includes the warning signs and what to do, with no padding.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для новоприбулих українців**

Провінційна рада Альберти Конгресу українців Канади (КУК) започаткувала в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів-наставників. Здебільшого це українські канадці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Наставник зустрічається з підопічним щонайменше двічі на місяць упродовж шести місяців. Він допомагає шукати роботу, визнавати кваліфікацію, орендувати житло та заповнювати урядові форми. Програму фінансує приватний фонд Prairie Bridges Foundation з Калгарі: він виділив 250 тис. доларів на два роки.

Заявки приймають і від новоприбулих, і від охочих стати наставниками — до 15 січня. «Багато хто приїхав із міцним фахом, але не знає, як тут усе працює, а пояснити нікому», — каже координаторка програми Галина Мороз (Halyna Moroz). За її словами, наставник заощаджує місяці спроб і помилок. Якщо вистачить коштів, наступного року програму розширять на Калгарі.

Judge: Accuracy: facts, numbers, dates and names match the source. Glossary terms are used correctly. "Кваліфіковані робітничі професії" is a reasonable rendering of "trades". The quote is slightly reworded ("пояснити нікому" for "nobody tells them") but the meaning is kept.

Language: mostly natural. "Урядові форми" is a calque of "government forms". "Урядові бланки", "анкети" or "документи" would be more idiomatic. "Заощаджує місяці спроб і помилок" is acceptable, but "економить" would read more smoothly.

Usefulness: clear and concise. It says what the program is and who it is for, and it gives the deadline. It does not say how to apply or whom to contact. The funding details sit awkwardly in the middle of the mentor-duties paragraph, before the deadline and the quote.

### ircc-cuaet-pr

**Канада відкриє новий шлях до постійного резидентства для українців, які приїхали за CUAET**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє новий шлях до постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Заявки почнуть приймати 2 березня, усього — до 10 000. Потрібен щонайменше рік роботи на повну ставку в Канаді після приїзду за CUAET і мовний тест не нижче CLB 5 з англійської або NCLC 5 з французької. До заявки можна включити членів родини, які живуть у Канаді. Той, хто подається поза Квебеком, має й жити поза Квебеком: ця провінція сама відбирає іммігрантів. Посібник із заповнення заявки та перелік потрібних документів міністерство оприлюднить за два тижні до старту.

Конгрес українців Канади (Ukrainian Canadian Congress, КУК) вітає рішення, але вважає ліміт замалим. За даними організації, з 2022 року за CUAET приїхали понад 300 000 українців, і десятки тисяч із них досі мають тимчасовий статус.

Failed checks: form: title too long

Judge: Accuracy: the headline and lead say Canada "opens" the pathway, but the post says "відкриє" (will open) and the source says it opens, with applications starting March 2. That is acceptable, not an error. The real slip is "Той, хто подається поза Квебеком, має й жити поза Квебеком". It is faithful in meaning, but "ця провінція сама відбирає іммігрантів" is a loose rendering of "runs its own selection". Also, "Ukrainian Canadian Congress, КУК" adds an English name that the glossary does not require; "Конгрес українців Канади (КУК)" would suffice. The source says "up to 10,000 applications", and "усього — до 10 000" is fine. The source says the CUAET work experience must be gained after arrival, and the post conveys that. The source says Quebec "runs its own selection", and the post's "відбирає іммігрантів" is close but a bit imprecise. Minor: the post omits that the "March 2" date has no year, which matches the source. Language: mostly natural. "Заявки почнуть приймати" is fine. "Посібник із заповнення заявки" is a slight expansion of "application guide". "Вітає рішення" is slightly off, since the source says "welcomed the announcement" (past tense). "Приїхали за CUAET" in the headline lacks "програмою", so the glossary form is not used on first mention in the headline. The lead uses the glossary names correctly. Usefulness: clear and concise. It states what happened and the conditions. It does not explain how this matters to the audience beyond the conditions, and the "PR" abbreviation is not explained as the status. It is a bit dense in the middle paragraph, which is one block of many conditions.

### statcan-population

**Населення Канади в третьому кварталі зросло лише на 0,2 %**

Це найповільніше зростання за третій квартал від 2020 року, повідомило в середу Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні налічувалося 41,7 млн осіб.

Населення зростало майже винятково завдяки новим постійним резидентам. Кількість непостійних резидентів, до яких належать іноземні студенти й тимчасові працівники, скоротилася на 65 тисяч. Це сталося після того, як за останні два роки Оттава обмежила видачу дозволів на навчання та змінила програми тимчасової роботи. Федеральний уряд заявляє, що хоче зменшити частку тимчасових резидентів у населенні.

Серед провінцій найшвидше зросла Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст був меншим за 0,1 %.

Економісти кажуть, що повільніше зростання може послабити тиск на ціни оренди у великих містах. Водночас нестача працівників у медицині та будівництві може посилитися.

Judge: Accuracy: "найповільніше зростання за третій квартал від 2020 року" is fine. Minor: the source says "the slowest pace for that period since 2020"; the post's "від 2020 року" is slightly ambiguous (should be "з 2020 року"). Also "Це сталося після того, як..." slightly overstates causality, while the source says "follows caps/changes announced"; and "обмежила видачу" is OK. "Федеральний уряд заявляє" fine. Source says "changes announced", post says Ottawa already restricted/changed – minor shift. Language: "від 2020 року" is a calque/wrong preposition (should be "з 2020 року"); "майже винятково" is okay, though "майже виключно" is more standard; "іноземні студенти й тимчасові працівники" omits "foreign" for workers (the source says temporary foreign workers) – minor. "Кількість... скоротилася на 65 тисяч" fine. Glossary: Statistics Canada name used correctly. Usefulness: clear and concise, but no explicit explanation of why it matters for Ukrainians in Canada (e.g., Ukrainians on temporary status such as CUAET); only generic economic effects. Headline "лише" adds slight editorializing.

### akwesasne-policing

**Поліція могавків Аквесасне й OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) підписали п'ятирічну угоду про поліцейське обслуговування вартістю 12 млн доларів. Про це в понеділок повідомила рада.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й шосе поблизу громади. Її територія лежить на межі Онтаріо, Квебеку та штату Нью-Йорк. Гроші підуть також на новий поліцейський відділок на острові Корнволл (Cornwall Island) і навчання восьми нових офіцерів. За словами OPP, влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці на воді.

Головна вождиня Лора Бенедикт (Laura Benedict) зазначила, що угода визнає поліцію могавків першою службою, яка реагує на виклики в громаді. «Наші офіцери знають ці води й ці родини. Тепер у них є ресурси, щоб робити свою роботу», — сказала вона.

Judge: Accuracy: no invented facts, but there are small distortions. "Grand Chief" is rendered as "Головна вождиня", which is acceptable. "Тепер у них є ресурси" adds "now" and slightly changes "This gives them the resources". The source says the OPP said the patrols focus on smuggling and boating safety "in the summer months". The post attributes this correctly but loosely, with "влітку" placed ahead of the focus. The post says "поліцію могавків першою службою, яка реагує на виклики", which is a reasonable rendering of "first responders". "Training eight new officers" is fine. The phrase "Cornwall Island" is rendered "острів Корнволл", which is a transliteration. The established Ukrainian form is "Корнволл", so this is acceptable.

Language: The text is mostly natural. "Поліцейське обслуговування" is a bit of a calque from "policing". "Офіцери" for police officers is an anglicism, and "поліцейські" would be more natural. "Головна вождиня" is slightly awkward. The headline uses the Latin "OPP" without Ukrainian on first mention, but the glossary allows the abbreviation in parentheses. The headline should use the glossary name. The phrase "Її територія лежить на межі" is fine. "Спільно патрулюватимуть" is good.

Usefulness: The post is clear and concise. It does not explain why it matters to Ukrainians in Canada, but it also adds no padding. The OPP abbreviation is not explained in the headline. Overall it is a decent news summary with no context for the audience."

### quebec-museum

**Музей сучасного мистецтва Монреаля відкривається після реконструкції виставкою художниці з Харкова**

Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal) у суботу знову відкриє двері для відвідувачів. Реконструкція будівлі в комплексі Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Площа виставкових залів збільшилася на 2000 квадратних метрів. З'явилися новий вхід з вулиці Сент-Катрін (Sainte-Catherine) і безкоштовна громадська тераса. Першої неділі кожного місяця вхід до музею буде безкоштовним.

Оновлений простір відкриває виставка художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а в Монреалі живе з 1998 року. Експозиція налічує 60 робіт, серед них серія великих полотен, створених після поїздки до рідного міста 2023 року. «Я хотіла, щоб люди побачили Харків як місто світла, студентів і музики, а не лише як місце з випусків новин», — сказала Лисенко на передпоказі в четвер.

Виставка триватиме до 12 квітня.

Judge: Facts all match the source (dates, numbers, quote, names). Minor issues: the headline calls her "художниця з Харкова", though she was born there and has lived in Montreal since 1998, so it blurs her current base. "40 млн доларів" does not say Canadian dollars, which is ambiguous for a Canadian audience. The phrase "місце з випусків новин" is slightly clumsy and calques "a place on the news"; "місце з новин" would be more natural. "Survey of the work" is rendered only as "виставка", losing the retrospective sense. The post is clear and concise but does not spell out why this matters to Ukrainians in Canada beyond the Kharkiv link.

### cra-ccb-tips

**Без декларації допомога на дітей припиниться з липня**

Агенція доходів Канади (CRA) нагадує: щоб без перерви отримувати канадську допомогу на дітей (CCB), сім'ї мають подати податкову декларацію до 30 квітня. Це стосується й тих, хто торік не мав доходу. Розмір допомоги щороку в липні перераховують за чистим доходом сім'ї за попередній рік. Якщо в CRA немає декларації когось із батьків, виплати з липня зупинять, доки її не подадуть і не опрацюють.

Новоприбулі, які ще не оформили допомогу, можуть подати заявку в особистому кабінеті CRA My Account після отримання номера соціального страхування (SIN). Є й поштовий варіант: форма RC66 разом із формою RC66SCH, у якій запитують про статус резидента й доходи за межами Канади. Безкоштовно подати декларацію допоможуть волонтерські податкові клініки для людей зі скромним доходом. За даними агенції, максимальна допомога на дитину віком до шести років наразі становить 8157 доларів на рік.

Що можна зробити:
• Подайте податкову декларацію до 30 квітня, навіть якщо торік не мали доходу, — і за себе, і за партнера чи партнерку.
• Якщо ви нещодавно приїхали й ще не оформили допомогу, подайте заявку одразу після отримання номера соціального страхування (SIN).
• Безкоштовно допоможуть волонтерські податкові клініки для людей зі скромним доходом — шукайте їх на сайті Агенції доходів Канади (CRA).
• Якщо виплата не надійшла, перевірте в особистому кабінеті CRA My Account, чи опрацьовано декларації обох батьків.

Judge: Accuracy: the bullet list adds claims not in the source: that the volunteer tax clinics can be found on the CRA website, and that My Account shows whether both parents' returns were processed. The source says neither. The post also drops the "2026" return year, which is minor. Language: "скромним доходом" is a calque of "modest income", and "невисоким" would be more natural. The full glossary names (CRA, SIN) are repeated in the bullets after the first mention. Usefulness: the "Що можна зробити" list mostly repeats the body text (the April 30 deadline, newcomers applying after getting a SIN, the free clinics), so it reads as padding. The lead and the key facts are clear.

### health-canada-recall-tips

**Maple Meadow відкликає дитячу суміш через ризик бактерії Cronobacter**

Міністерство охорони здоров'я Канади (Health Canada) закликає батьків припинити користуватися трьома партіями сухої дитячої суміші Maple Meadow. У продукті може бути бактерія Cronobacter. Випадків захворювання поки не зафіксовано.

Відкликання стосується банок по 800 грамів, які продавали в продуктових магазинах і аптеках по всій країні. Дата «найкраще вжити до» — червень 2027 року. Коди партій надруковані на денці кожної банки.

Інфекція Cronobacter трапляється рідко, але може бути небезпечною для новонароджених, особливо недоношених або з ослабленим імунітетом. Її ознаки: гарячка, погана охота до їжі, незвичний плач і сильна кволість.

Відкликаною сумішшю не можна годувати дітей. Банку варто повернути в магазин, де її купили, і отримати гроші назад. Якщо після суміші в дитини з'явилися симптоми, негайно зверніться до лікаря або зателефонуйте на номер 811.

Що можна зробити:
• Перегляньте на денці банки код партії та дату «найкраще вжити до» і порівняйте їх зі списком відкликаних партій на сайті міністерства охорони здоров'я Канади (Health Canada).
• Не годуйте дитину сумішшю з відкликаних партій. Поверніть банку в магазин, де її купили, і отримайте гроші назад.
• Якщо після суміші в дитини з'явилися гарячка, погана охота до їжі, незвичний плач або сильна кволість, негайно зверніться до лікаря або зателефонуйте на номер 811.

Judge: Accuracy: the post says the formula was sold "по всій країні", which matches "across Canada". It adds "на сайті ... зі списком відкликаних партій", but the source never mentions a website or a list of recalled lots. That is a minor invented detail. The source says lot codes are on the bottom of the can, but it doesn't say the best-before date is there. The post's call to check the date at the bottom is a small distortion.

Language: the post is mostly natural. "Погана охота до їжі" is slightly awkward, and "відмова від їжі" or "поганий апетит" would be better. "Сильна кволість" is acceptable. "Гарячка" is fine, though "температура" is more common. The glossary form is used correctly on first mention. Later in the text, "міністерство охорони здоров'я Канади (Health Canada)" is repeated in full, which is clumsy. The headline keeps "Cronobacter" in Latin, which is acceptable.

Usefulness: the content is clear and relevant. The "Що можна зробити" list repeats the body almost word for word: returning the can, the symptoms and 811 all appear twice. That is padding and repetition. The post also never says the 811 line is a Canadian health line, which could help newcomers. The post doesn't say that the lot codes themselves weren't provided in the source, so readers can't check them unless they go to an outside source.

