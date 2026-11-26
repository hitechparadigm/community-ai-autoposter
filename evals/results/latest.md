# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `b322665a` · 9/9 posts written · **7/9 passed every check** · 38 Claude calls · $0.47 ($0.052 per post)

| Check | Pass rate |
| --- | --- |
| facts | 100% |
| glossary | 89% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 100% |
| reviewer | 100% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.22 |
| language | 4.00 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/3 |
| cra-ccb-tips | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |

## Details

### min-wage-mb

**У Манітобі мінімальну зарплату підвищать до 16,50 долара**

Від 1 жовтня мінімальна оплата праці в Манітобі становитиме 16,50 долара за годину. Про це у вівторок оголосив уряд провінції. Ставка зросте на 65 центів.

Підвищення прив'язане до інфляції в провінції, як вимагає закон 2023 року. Міністр праці Деніел Моро (Daniel Moreau) сказав, що мінімальну зарплату отримують близько 40 тисяч людей, здебільшого в роздрібній торгівлі та закладах харчування. За його словами, родини досі відчувають подорожчання продуктів і оренди.

Торгова палата Манітоби (Manitoba Chambers of Commerce) заявила, що малий бізнес візьме додаткові витрати на себе, але попросила в майбутньому попереджати роботодавців завчасніше. Багато її членів і так платять більше за мінімум.

Ставка в Манітобі залишиться нижчою, ніж у Британській Колумбії, і вищою, ніж у Саскачевані. Нова ставка діє для всіх годин, відпрацьованих від 1 жовтня, зокрема для студентів і працівників із неповним робочим днем.

Judge: Facts match the source: the rate, the 65-cent rise, the date, 40,000 workers, the 2023 law, the minister's name, the Chambers of Commerce and the comparison with BC and Saskatchewan. Language problems: "оплата праці" is fine, but "мінімальну зарплату отримують" is slightly clumsy. "платять більше за мінімум" is a calque and should be "платять більше за мінімальну ставку" or "вище за мінімум". "візьме додаткові витрати на себе" is acceptable, though "покриє" would be more natural. "закладах харчування" is fine. "Деніел Моро" is acceptable. Usefulness: clear and concise. It leaves out the previous rate ($15.85) but the source doesn't give it either. It has no practical "what to do" note, but this isn't required.

### rcmp-deepfake

**У Метро-Ванкувері шахраї використовують дипфейки в романтичних аферах**

Канадська королівська кінна поліція (RCMP) попереджає мешканців Метро-Ванкувера про романтичні афери. У них шахраї видають себе за інших людей за допомогою відео, створеного штучним інтелектом.

Цього року про втрати повідомили 85 осіб, разом вони позбулися 2,3 млн доларів. У більшості випадків шахрай знайомиться з жертвою в застосунку для знайомств або в соцмережі, а потім влаштовує короткі відеодзвінки. Підроблені обличчя й голос роблять вигадану особу переконливою. «Дзвінки виглядають справжніми, і саме тому такі афери працюють», — каже сержантка Прія Сандху (Priya Sandhu) з відділу фінансових злочинів у Суррі (Surrey). Коли довіра з'являється, починаються прохання про гроші: на лікування, через заблокований рахунок або для вигідної інвестиції.

Поліція називає такі тривожні ознаки: співрозмовник не може зустрітися наживо, дзвінок раптово уривається, коли його просять повернути голову, просять надіслати криптовалюту чи подарункові картки. Якщо гроші вже переказано, одразу зверніться до банку, а також повідомте місцеву поліцію й Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Accuracy: "85 people reported losing a combined $2.3 million" is rendered okay, but "доларів" does not specify Canadian dollars (the source doesn't either). The "so far this year" is "Цього року" (acceptable). "Загалом/на лікування" fine ("medical emergency" → "на лікування" is a slight narrowing). "Ends abruptly when asked to turn their head" OK. "In most cases" OK. Language: "Метро-Ванкувер" is acceptable, though "Метро-Ванкувера" in the second sentence is inconsistent with the title's locative form; "афери працюють" and "Коли довіра з'являється" are slightly stiff; "позбулися" is fine. "Просять надіслати" lacks a clear subject (impersonal) and parallelism with "співрозмовник не може". Usefulness: clear and relevant, but no extra practical advice. The gender of Sgt. Sandhu ("сержантка") is assumed; the source doesn't state gender (though "Priya" is typically female). Original also says "financial crime unit in Surrey" – fine.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для новоприбулих українців**

Провінційна рада Конгресу українців Канади (КУК) в Альберті запустила в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET. Новоприбулим допомагатимуть 120 волонтерів-наставників.

Більшість із них — канадці українського походження, які працюють у робітничих професіях, медицині та інженерії. Наставник зустрічається зі своїм підопічним щонайменше двічі на місяць протягом півроку. Він допомагає шукати роботу, визнавати кваліфікацію, орендувати житло та заповнювати урядові форми. Програму фінансує приватний фонд Prairie Bridges Foundation з Калгарі: він виділив на два роки 250 тисяч доларів.

Координаторка програми Галина Мороз (Halyna Moroz) пояснює: багато хто приїхав із добрим фахом, але не знає, як тут усе влаштовано, а підказати нікому. Наставник, за її словами, економить місяці спроб і помилок.

Заявки від новоприбулих і від охочих стати наставниками приймають до 15 січня. Наступного року рада планує поширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts match the source (120 mentors, twice a month for six months, $250,000 over two years, Jan 15, Calgary expansion, glossary names). Language: "урядові форми" is a slight calque (better "урядові бланки/анкети/документи"). "робітничі професії" is imprecise for "trades" (better "кваліфіковані робітничі професії/ремесла"). The "Програму фінансує... він виділив" sequence is slightly clunky. Usefulness: clear and concise, but gives no hint about how to apply and has no practical "what to do" step. The source has none either, so this is a minor point.

### ircc-cuaet-pr

**Для українців із CUAET відкриють шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову програму постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер. Заявки почнуть приймати 2 березня.

Міністерство імміграції Канади прийме до 10 000 заявок. Потрібен щонайменше рік роботи на повну ставку в Канаді після приїзду за CUAET і результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. До заявки можна включити членів родини, які перебувають у Канаді. Заявники, які живуть поза Квебеком, мають також планувати жити поза ним, бо Квебек відбирає іммігрантів самостійно.

Посібник для заявників і перелік потрібних документів міністерство опублікує за два тижні до старту.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхало понад 300 000 українців. За даними КУК, десятки тисяч із них досі мають тимчасовий статус.

Judge: Accuracy: facts match the source. Minor: "Заявники... мають планувати жити поза ним, бо Квебек відбирає іммігрантів самостійно" is fine. "Шлях" in headline vs "програма" in body: the source says "pathway", so "програма" slightly shifts the meaning. "Заявки почнуть приймати 2 березня" is correct; the source says "starting March 2". The headline "відкриють" is fine. The post does not say the year-long work must be full-time work gained after arrival under CUAET, but it does say so. Language: mostly natural. "Міністерство імміграції Канади прийме" repeats the ministry name right after the first sentence, which is a bit heavy. "замалим" is colloquial. "перелік потрібних документів" is fine. "Посібник для заявників" is a decent rendering of "application guide". "Програма" for "pathway" is a minor word-choice issue. Usefulness: clear and informative, with no padding. Order puts the CUAET Congress reaction last, which is fine. It lacks a "what to do" section, but one is not required. The wording "ліміт замалий" is slightly weak. Overall good but not publish-unchanged because of the repetition and the "програма" vs "pathway" choice.

### statcan-population

**Населення Канади зросло лише на 0,2% — найповільніше з 2020 року**

У третьому кварталі населення Канади збільшилося на 0,2%. Для цього періоду це найповільніше зростання з 2020 року, повідомило Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні проживало 41,7 млн осіб.

Приріст майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, зокрема іноземних студентів і тимчасових працівників, скоротилася на 65 тисяч. Це наслідок обмежень на видачу дозволів на навчання та змін у програмах тимчасової праці, які Оттава запровадила за останні два роки. Федеральний уряд хоче, щоб частка тимчасових резидентів у населенні зменшилася.

Найшвидше серед провінцій зростала Альберта — на 0,5%. В Онтаріо та Британській Колумбії приріст був меншим за 0,1%.

Економісти зазначають, що повільніше зростання населення зменшить тиск на ціни оренди у великих містах. Водночас може загостритися нестача працівників у медицині та будівництві.

Judge: Accuracy: the headline drops the "for the third quarter" qualifier, so "slowest since 2020" reads as a general claim. The body states it correctly. "Це наслідок" presents the cause as certain, while the source only says the decline "follows" the caps. "Запровадила" (introduced) differs slightly from "announced". Language: "медицині" is acceptable, but "охороні здоров'я" is more standard for "health care". "Для цього періоду це найповільніше зростання" is a little clunky and calqued from English. Usefulness: the post is clear and concise and has no padding. It does not say what this means for Ukrainians in Canada, such as study permits, work permits or the rental market. Glossary names are used correctly.

### akwesasne-policing

**Могавки й OPP уклали угоду про поліцію на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) підписали п'ятирічну угоду про поліцейське обслуговування вартістю 12 млн доларів. Про це в понеділок повідомила рада.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й автотраси поблизу громади. Вона розташована на межі Онтаріо, Квебеку та штату Нью-Йорк. Гроші підуть також на новий відділ поліції на острові Корнволл (Cornwall Island) і навчання восьми нових поліцейських.

За словами OPP, влітку спільні патрулі зосередяться на боротьбі з контрабандою та безпеці на воді.

Верховна вождиня Лора Бенедикт (Laura Benedict) наголосила, що угода визнає: поліція могавків першою реагує на події в громаді. «Наші поліцейські знають ці води й ці родини. Це дає їм ресурси, щоб робити свою справу», — сказала вона.

Judge: Accuracy: the facts match the source, with small shifts. "Автотраси" is fine for highways. "Mohawk police are the first responders" became "першою реагує на події", which is acceptable. "Mohawk Council of Akwesasne" became "Рада могавків Аквесасне", which is fine. "Відділ поліції" for "police station" is slightly off, since "поліцейська дільниця" or "відділення" is more natural. "Вона розташована на межі" refers to the community, but the antecedent is ambiguous after the long list of subjects, and "straddles the borders" is slightly weakened. The post also doesn't say the deal covers the river and highways "near the community" in the same way, though it comes close. Language: the headline "Могавки й OPP" is acceptable, but it leaves out the Mohawk police service and uses the abbreviation without expansion. "Поліцейське обслуговування" is a bit bureaucratic. "Острів Корнволл" is fine, though "Корнуолл" is the usual Ukrainian rendering. The abbreviation OPP is kept in Latin letters per the glossary. Usefulness: the post says what happened but not why it matters to Ukrainians in Canada. It has no context and no explanation of the Akwesasne community. The quote order was changed and the sentence about the OPP patrols was moved, which is fine.

### quebec-museum

**Музей сучасного мистецтва Монреаля відкривається після ремонту за 40 млн доларів**

Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal) знову відкривається для відвідувачів у суботу. Його будівлю на Place des Arts чотири роки реконструювали, а робота коштувала 40 млн доларів.

Галерейна площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з боку вулиці Сент-Катрін і безкоштовна публічна тераса. Першої неділі кожного місяця вхід до музею буде вільний.

Першою виставкою стала ретроспектива художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а в Монреалі живе з 1998 року. В експозиції 60 робіт, серед них серія великих полотен, які Лисенко створила після поїздки до рідного міста 2023 року. «Я хотіла, щоб люди бачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала художниця на попередньому показі в четвер.

Виставка триватиме до 12 квітня.

Judge: Accuracy: "survey" rendered as "ретроспектива" (a retrospective is a specific kind of survey; mild shift). "Реконструювали" for "renovation" is fine. Name "Катерина Лисенко" is a transliteration from the English/Russian-style spelling "Lysenko"; the Ukrainian "Kateryna" would be "Катерина", and "Лисенко" is fine, so this is OK. Language: "ремонту" in the headline undersells a four-year renovation (a "реконструкція" would be better); "робота коштувала" is awkward; "вхід буде вільний" is a bit stiff; "Першою виставкою" should be "Відкриває музей виставка"; "2023 року" is fine. Usefulness: the post gives the facts but lacks a link to the Ukrainian audience beyond Kharkiv (e.g., the Ukrainian-born artist angle isn't highlighted), no practical details such as the ticket price or address; the opening date is just "Saturday" with no date. Also the Kharkiv quote is not tied to why it matters to the audience.

### cra-ccb-tips

**Без декларації до 30 квітня родинам можуть призупинити допомогу на дітей**

Агенція доходів Канади (CRA) нагадала родинам: щоб канадська допомога на дітей (CCB) надходила без перерв, податкову декларацію потрібно подати до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку в липні перераховують за чистим доходом родини за попередній рік. Якщо в CRA немає декларації від обох батьків, виплати з липня зупиняють, доки декларацію не подадуть і не опрацюють. Максимальна допомога на дитину до шести років нині становить 8 157 доларів на рік.

Що можна зробити:
• Домовтеся з чоловіком чи дружиною (партнером чи партнеркою), щоб обоє подали декларації до 30 квітня.
• Якщо ви нещодавно приїхали й ще не оформили CCB, подайте заявку в CRA My Account, щойно отримаєте SIN.
• Заявку можна надіслати й поштою: форма RC66 разом із RC66SCH, де запитують про статус резидентства та доходи за межами Канади.
• Якщо дохід невисокий і потрібна допомога із заповненням, зверніться до громадської волонтерської податкової клініки: там подадуть декларацію безкоштовно.

Failed checks: glossary: not used: номер соціального страхування (SIN)

Judge: Glossary violation: SIN is used on first mention without the required "номер соціального страхування (SIN)". Awkward phrasing "з чоловіком чи дружиною (партнером чи партнеркою)" is clumsy and wordy. The "подадуть декларацію безкоштовно" and the "if income is modest" condition are loosely rendered from the source but acceptable. The source's "2026 return" year is omitted, which is minor. The first bullet is generic advice but safe. Otherwise the facts (April 30, July recalculation, both parents' returns, RC66/RC66SCH, $8,157) match.

### health-canada-recall-tips

**Maple Meadow: у Канаді відкликали три партії дитячої суміші**

Міністерство охорони здоров'я Канади (Health Canada) радить батькам припинити використовувати три партії сухої дитячої суміші Maple Meadow. Вони можуть бути заражені бактерією Cronobacter. Банки по 800 грамів продавали в продуктових крамницях і аптеках по всій країні. Термін придатності в них спливає в червні 2027 року. Коди партій надруковані на денці кожної банки. Про випадки захворювання не повідомляли.

Інфекція, яку спричиняє Cronobacter, трапляється рідко, але для немовлят вона може бути небезпечною. Найбільший ризик — для недоношених дітей і малюків з ослабленим імунітетом. Симптоми: гарячка, поганий апетит, незвичний плач і сильна кволість.

Відкликану суміш не можна давати дітям. Її можна повернути в крамницю, де купили, і отримати гроші. Якщо в дитини після такої суміші з'явилися симптоми, негайно зверніться до лікаря або зателефонуйте на 811.

Що можна зробити:
• Огляньте банки Maple Meadow вдома: знайдіть код партії на денці та звірте його з кодами у повідомленні про відкликання.
• Банку з відкликаної партії приберіть подалі від інших, щоб її випадково не відкрили. Суміш для дитини самі не готуйте, а про заміну спитайте лікаря чи фармацевта.
• Віднесіть таку банку в крамницю, де її купили, і попросіть повернути гроші.
• Якщо дитина вже пила цю суміш, стежте за її станом. Коли з'являться симптоми, телефонуйте лікареві або на 811 і скажіть, яку суміш їла дитина.

Judge: Accuracy: "best-before" rendered as "термін придатності" (expiry), a slight shift in meaning (better: "найкраще спожити до"). Other facts match. The advice list is general and safe, no invented specifics.
Language: "радить... припинити використовувати" is clumsy; "суміш, яку їла дитина" should be "пила"; "Суміш для дитини самі не готуйте" is ambiguous (reads like homemade formula); "не можна давати дітям" is less precise than "немовлятам".
Usefulness: the text repeats the return-to-store and symptoms/811 advice in both the main text and the list. The "Що можна зробити" list is mostly a rehash of the body. The "звірте з кодами у повідомленні про відкликання" step is useful, but the source gives no codes or link.

