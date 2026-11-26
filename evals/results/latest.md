# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `53ee127c` · 9/9 posts written · **4/9 passed every check** · 42 Claude calls · $0.53 ($0.059 per post)

| Check | Pass rate |
| --- | --- |
| facts | 89% |
| glossary | 100% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 100% |
| reviewer | 89% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.11 |
| language | 4.00 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 5/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/4 |

## Details

### min-wage-mb

**У Манітобі мінімальну зарплату підвищать до 16,50 долара на годину**

Уряд Манітоби у вівторок оголосив, що з 1 жовтня мінімальна оплата праці в провінції становитиме 16,50 долара на годину. Це на 65 центів більше, ніж зараз.

Підвищення прив'язане до рівня інфляції в провінції, як вимагає закон, ухвалений 2023 року. За словами міністра праці Деніела Моро (Daniel Moreau), мінімальну зарплату отримують близько 40 тисяч працівників, здебільшого в роздрібній торгівлі та закладах харчування. «Родини й досі відчувають, як дорожчають продукти й оренда, а ця зміна дає змогу зарплатам не відставати від цін», — сказав він на пресконференції у Вінніпезі.

Роботодавці мають оновити оплату за всі години, відпрацьовані з 1 жовтня, зокрема для студентів і працівників на неповну ставку. Ставка в Манітобі й надалі буде нижчою, ніж у Британській Колумбії, але вищою, ніж у Саскачевані.

Торгово-промислова палата Манітоби (Manitoba Chambers of Commerce) каже, що малий бізнес візьме додаткові витрати на себе, але просить уряд у наступні роки повідомляти роботодавців про зміни завчасніше. Багато її членів і так платять більше за мінімум, щоб залучити працівників.

Judge: Accuracy: the facts match the source. One minor issue is "Це на 65 центів більше, ніж зараз". It is implied by the source but not stated as "now". "Деніела Моро (Daniel Moreau)" is fine. "Торгово-промислова палата Манітоби" is a loose rendering of "Manitoba Chambers of Commerce", which is plural and more generally means chambers of commerce. Language: "візьме додаткові витрати на себе" is slightly calqued, and "додаткові" is not in the source. "платять більше за мінімум" is awkward, and "понад мінімум" or "вище за мінімум" would be better. "мінімальну зарплату отримують" is acceptable. "закладах харчування" is fine. "Ставка ... буде нижчою, ніж" is correct. Usefulness: clear and concise, but it has no "what to do" or practical note for readers, for example for workers or employers. The lead is good. The order of the paragraphs is fine.

### rcmp-deepfake

**RCMP попередила про романтичні шахрайства з дипфейками в Метро-Ванкувері**

Канадська королівська кінна поліція (RCMP) застерігає мешканців Метро-Ванкувера від романтичних шахрайств, у яких аферисти видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

За даними слідчих, цьогоріч про втрати повідомили 85 осіб. Разом вони втратили 2,3 млн доларів. Здебільшого шахраї знайомилися з жертвою в застосунку для знайомств або в соцмережах, а потім влаштовували короткі відеодзвінки. Підроблені обличчя й голос робили фальшиву особу переконливою. Щойно з'являлася довіра, починалися прохання про гроші: на лікування, через заблокований банківський рахунок або заради вигідної інвестиції.

Сержантка Прія Сандгу (Priya Sandhu) з відділу фінансових злочинів RCMP у Сурреї каже, що саме реалістичність дзвінків робить такі схеми ефективними: «Дзвінки виглядають справжніми».

Поліція називає тривожні ознаки: співрозмовник не може зустрітися наживо, дзвінок раптово уривається, коли його просять повернути голову, а ще він просить криптовалюту чи подарункові картки. Той, хто вже надіслав гроші, має негайно зв'язатися з банком і повідомити місцеву поліцію та Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: "Sandhu" rendered as "Сандгу", which is a questionable transliteration (should be "Сандгу"/"Сандху"; Ukrainian usually "Сандху"). Headline says "RCMP" without glossary form in the headline, though the glossary applies to first mention and the headline uses RCMP only (possible issue). "Метро-Ванкувері" vs "Метро-Ванкувера": inconsistent forms. "Втрати повідомили 85 осіб" is slightly distorted: the source says 85 people reported losing money. "на лікування" narrows "medical emergency". "Здебільшого" is fine. The quote is truncated and the paraphrase of the quote is repetitive ("реалістичність... Дзвінки виглядають справжніми"). Language: "аферисти" and "шахраї" are fine; "видають себе за інших людей" fine; "створеного штучним інтелектом" fine; "Канадський антишахрайський центр" is acceptable but not an official Ukrainian name. "Сержантка" is fine. "наживо" is slightly colloquial. Usefulness: clear, but lacks advice to avoid being scammed beyond the warning signs, and the quote loses the 'once trust is built' part; the 'what to do' step is covered. Overall the post is good but not publish-ready unchanged.

### ucc-mentorship

**В Едмонтоні запустили менторську програму для українців, які приїхали за CUAET**

Провінційна рада Альберти Конгресу українців Канади (КУК) запустила в Едмонтоні менторську програму для тих, хто приїхав до Канади за програмою CUAET.

Новоприбулих поєднали зі 120 волонтерами-менторами. Здебільшого це українські канадці, які працюють у кваліфікованих робітничих професіях, медицині та інженерії. Наставник зустрічається з підопічним щонайменше двічі на місяць упродовж півроку. Він допомагає шукати роботу, визнавати кваліфікацію, орендувати житло й заповнювати документи для державних установ.

Програму фінансує Prairie Bridges Foundation — приватний фонд із Калгарі. Він виділив на два роки 250 тисяч доларів.

«Багато хто приїхав із добрим фахом, але не знає, як тут усе влаштовано, а пояснити нікому, — каже координаторка програми Галина Мороз (Halyna Moroz). — Ментор заощаджує місяці спроб і помилок».

Заявки від новоприбулих і від охочих стати менторами приймають до 15 січня. Наступного року КУК планує розширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts match the source: 120 mentors, twice a month for six months, $250,000 over two years, 15 January deadline, expansion to Calgary. Minor issues: (1) The headline says "за CUAET" without the glossary form "програма CUAET". The body has "за програмою CUAET". (2) "поєднали зі 120 волонтерами-менторами" is slightly awkward, and "закріпили за" or "підібрали" would be more natural. (3) The last sentence says "КУК планує" where the source says the provincial council. This is a very small simplification. (4) The post gives no practical next step for readers, such as how to apply, and the source doesn't say. (5) "Prairie Bridges Foundation" stays in Latin script, which is acceptable. Overall the post is clear and concise, but I wouldn't publish it unchanged because of the headline glossary form and the "поєднали" wording.

### ircc-cuaet-pr

**Для українців із CUAET відкриють шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову можливість отримати постійне резидентство (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Заявки прийматимуть з 2 березня, до 10 000 заяв. Кандидатам потрібен щонайменше рік роботи на повну ставку в Канаді, здобутий після приїзду за CUAET. Також треба підтвердити знання мови: не менш як 5 балів за канадською шкалою CLB (англійська) або NCLC (французька). До заявки можна включити членів родини, які перебувають у Канаді. Ті, хто подається не з Квебеку, мають планувати жити поза межами провінції: Квебек відбирає іммігрантів самостійно.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхали понад 300 000 українців, і, за даними КУК, десятки тисяч із них досі мають тимчасовий статус.

Посібник із подання заявки та перелік потрібних документів міністерство імміграції Канади оприлюднить за два тижні до відкриття прийому.

Failed checks: facts: missing: CLB 5

Judge: Accuracy: the facts match the source (March 2, 10,000 cap, one year of full-time work, CLB/NCLC 5, family, Quebec, UCC, 300,000, two weeks). Minor slips: "Ті, хто подається не з Квебеку" is imprecise; the source says applicants outside Quebec. "Планувати жити поза межами провінції" is vague about which province. The source doesn't say that the work experience must be gained in Canada "after arrival" in the sense of "здобутий після приїзду", but this is fine. The post says "заявки прийматимуть з 2 березня, до 10 000 заяв", which is a clumsy phrasing; the cap should read "не більше 10 000 заяв". Language: "не менш як 5 балів за канадською шкалою CLB (англійська) або NCLC (французька)" is slightly awkward; NCLC is the Canadian language benchmark for French, not exactly a single "scale". "Відкриють шлях" in the headline is acceptable. "Посібник із подання заявки" is fine, but the mention of "міністерство імміграції Канади" repeated is OK per glossary. "Висока" no problems. Usefulness: clear and covers the key points, but lacks a clear statement that the pathway is only for those with work experience and doesn't explain the term "ліміт замалим" with context; no padding. The headline lacks a year or other context. Overall it is good but would need light editing for the cap phrasing and the Quebec sentence.

### statcan-population

**Населення Канади зросло лише на 0,2 %, тимчасових резидентів поменшало**

У третьому кварталі населення Канади збільшилося на 0,2 %. Це найповільніше зростання для цього періоду від 2020 року, повідомило Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні налічувалося 41,7 млн людей.

Приріст майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, до яких належать іноземні студенти й тимчасові працівники, скоротилася на 65 тисяч. Це сталося після того, як федеральна влада обмежила видачу дозволів на навчання та змінила програми тимчасової праці — ці рішення оголошували впродовж останніх двох років. Оттава хоче, щоб тимчасові резиденти становили меншу частку населення.

Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст був меншим за 0,1 %. Економісти кажуть, що повільніше зростання послабить тиск на ринок оренди у великих містах, але може загострити брак працівників у медицині та будівництві.

Judge: Facts, numbers and glossary term all match the source. Language: "від 2020 року" should be "з 2020 року" (calque of "since"). The headline verb "поменшало" is colloquial for a news headline. "Це сталося після того, як..." slightly strengthens "follows" into a causal link. Usefulness: clear and concise, but it doesn't say what this means for Ukrainians in Canada, such as temporary status holders. It also has no "what to do" section, which isn't required.

### akwesasne-policing

**Поліція могавків Аквесасне й OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про охорону правопорядку на 12 млн доларів. Про це рада повідомила в понеділок.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) і OPP спільно патрулюватимуть річку та шосе поблизу громади. Вона розташована на кордонах Онтаріо, Квебеку й штату Нью-Йорк. Кошти підуть також на новий відділок на острові Корнуолл (Cornwall Island) і навчання восьми нових поліцейських.

Головна вождиня Лора Бенедікт (Laura Benedict) наголосила, що угода визнає: поліція могавків першою реагує на події в громаді. «Наші поліцейські знають ці води й ці родини. Тепер вони матимуть ресурси, щоб робити свою справу», — сказала вона. У OPP пояснили, що влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці на воді.

Judge: Accuracy: mostly faithful. Minor slips: "summer months" is attached only to boating safety in the source, while the post says patrols focus on smuggling and water safety in summer, which slightly shifts the meaning. "Joint patrols on the river and highways" is fine. "Вона розташована" is ambiguous: its antecedent could be the police service or the community. The source says the community straddles the borders, and the post's "на кордонах" is acceptable. "Тепер вони матимуть" is a slight embellishment of "This gives them". Glossary: "Провінційна поліція Онтаріо (OPP)" is correct on first mention. "Могавки Аквесасне" is used as a name for the council, and "Поліція могавків Аквесасне" in the headline is acceptable. Language: generally natural. "Охорона правопорядку" is a bit bureaucratic for "policing". "Головна вождиня" is acceptable but "Grand Chief" is often rendered "великий вождь". Usefulness: clear and concise, but it gives no explanation of why it matters to Ukrainians in Canada, and it has no context. The post is only a plain news summary.

### quebec-museum

**Музей сучасного мистецтва Монреаля відкриється після реконструкції виставкою художниці з Харкова**

Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal) знову відкриється для відвідувачів у суботу. Його будівля на Place des Arts чотири роки була на реконструкції, яка коштувала 40 млн доларів.

Виставкова площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з боку вулиці Сент-Катрін і безкоштовна публічна тераса. Першої неділі кожного місяця вхід до музею безкоштовний.

Першою виставкою стане огляд творчості художниці Катерини Лисенко (Kateryna Lysenko), уродженки Харкова, яка живе в Монреалі з 1998 року. Вона об'єднує 60 робіт, зокрема серію великих полотен, створену після поїздки до рідного міста 2023 року. «Я хотіла, щоб люди побачили Харків містом світла, студентів і музики, а не лише місцем із новин», — сказала Лисенко на попередньому перегляді в четвер. Виставка триватиме до 12 квітня.

Failed checks: reviewer: Займенник «Вона» в реченні «Вона об'єднує 60 робіт» стосується художниці (останній підмет — «яка живе»), а не виставки, тож речення читається хибно. Треба написати «Виставка об'єднує 60 робіт» або «До неї ввійшли 60 робіт».

Judge: Facts match the source. Language: "Вона об'єднує 60 робіт" has an unclear antecedent. The preceding noun "огляд" is masculine, and "вона" could be read as referring to the artist. It needs rewording, e.g. "У виставці — 60 робіт". "Виставкова площа збільшилася на 2000 кв. м" is slightly stiff. Usefulness: clear and concise, and the Kharkiv link is relevant to the audience. It gives no practical details such as the address or ticket info. It doesn't spell out why it matters to Ukrainians in Canada.

### cra-ccb-tips

**Без декларації від липня припиняться виплати на дітей**

Агенція доходів Канади (CRA) нагадала сім'ям: щоб без перерв отримувати канадську допомогу на дітей (CCB), потрібно подати податкову декларацію до 30 квітня, навіть якщо торік доходу не було.

Розмір допомоги щороку в липні переглядають за чистим доходом сім'ї за попередній рік. Якщо в CRA немає декларацій обох батьків, виплати зупиняються в липні й відновлюються лише після того, як документи подадуть і обробять. Максимальна допомога на дитину до шести років нині становить 8157 доларів на рік.

Що можна зробити:
• Домовтеся з другим із батьків, щоб обидві декларації надійшли до CRA до 30 квітня, навіть якщо в когось не було доходу.
• Якщо ще не оформили CCB, подайте заявку через CRA My Account, щойно отримаєте номер соціального страхування (SIN).
• Заявку можна надіслати й поштою: форма RC66 разом із RC66SCH, де питають про статус резидентства та дохід за межами Канади.
• Якщо дохід невисокий, подайте декларацію безкоштовно в громадській податковій клініці, де працюють волонтери.

Judge: Facts, numbers, dates and form names match the source, and the glossary names are used correctly. Problems: (1) The headline is too absolute. Payments stop only if CRA has no return for both parents, but it reads as if any missing return stops them. (2) The first action item repeats the April 30 deadline and the no-income point from the lead. (3) The $8,157 maximum is only loosely relevant and sits awkwardly at the end of the paragraph about recalculation. (4) The action list never says the application route is aimed at newcomers. (5) "з другим із батьків" is slightly clumsy; "з другим з батьків" or "з іншим з батьків" would be smoother. (6) The source says "2026 return" while the post says "торік". This is acceptable but loses the year.

### health-canada-recall-tips

**У Канаді відкликали три партії дитячої суміші Maple Meadow**

Міністерство охорони здоров'я Канади (Health Canada) закликає батьків припинити користуватися трьома партіями сухої дитячої суміші Maple Meadow. У ній може бути бактерія Cronobacter.

Банки по 800 грамів продавали в продуктових крамницях і аптеках по всій Канаді. Термін придатності — червень 2027 року. Коди партій надруковано на денці банки. Про випадки захворювання не повідомляли.

Інфекція Cronobacter трапляється рідко, але може бути небезпечною для немовлят, особливо недоношених і дітей зі слабким імунітетом. Її ознаки — гарячка, дитина погано їсть, незвично плаче й дуже квола. Якщо такі симптоми з'явилися після того, як дитина випила суміш, негайно зверніться до лікаря або зателефонуйте на 811.

Відкликаною сумішшю дитину годувати не можна. Банку варто повернути в магазин, де її купили, і отримати гроші назад.

Що можна зробити:
• Перегляньте всі банки Maple Meadow удома й порівняйте код партії на денці з кодами у повідомленні про відкликання.
• Відкладіть відкликану банку окремо, щоб ніхто не скористався нею, поки ви не віднесете її до магазину. Збережіть чек, якщо він є.
• Якщо дитина вже пила суміш із цих партій, стежте за її станом. У разі сумнівів телефонуйте на 811.
• Не готуйте суміш удома й не шукайте замінників самотужки. Про безпечну заміну порадьтеся з сімейним лікарем або педіатром.

Judge: Accuracy: "Термін придатності" is fine for best-before. "Дитина... дуже квола" is okay but "very low energy" slightly altered. The source says "call a doctor or 811"; the post matches. Minor problem: the glossary name is used with a capital "Міністерство", whereas the glossary gives lowercase "міністерство" (a reviewer could flag it). Also "У ній може бути бактерія" is slightly vague. "Банку варто повернути... гроші назад" is colloquial. Advice list: "порівняйте код з кодами у повідомленні про відкликання" is fine, but the post never gives the lot codes, and it does not say where to find them. This is a usefulness gap. "Не готуйте суміш удома" is an unsupported, odd piece of advice (homemade formula is unsafe, but the point is unclear). Repetition: the 811/symptoms point appears twice. "Отримати гроші назад" is a little calque-like; "відшкодування" would read better. "Зверніться/зателефонуйте" shifts from the third-person register. "Банки продавали" is fine.

