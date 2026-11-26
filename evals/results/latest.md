# Evaluation results

2026-11-26 · model `claude-sonnet-5-5` · prompts `a7b6eb86` · 9/9 posts written · **6/9 passed every check** · 42 Claude calls · $0.56 ($0.062 per post)

| Check | Pass rate |
| --- | --- |
| facts | 89% |
| glossary | 89% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 100% |
| reviewer | 100% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 3.89 |
| language | 4.11 |
| usefulness | 3.89 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/5/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 3/4/3 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |

## Details

### min-wage-mb

**У Манітобі мінімальна зарплата зросте до 16,50 долара за годину**

Мінімальна оплата праці в Манітобі від 1 жовтня становитиме 16,50 долара за годину. Про це у вівторок повідомив уряд провінції. Ставка зросте на 65 центів.

Підвищення прив'язане до інфляції в провінції — цього вимагає закон, ухвалений 2023 року. За словами міністра праці Деніела Моро (Daniel Moreau), мінімальну зарплату отримують близько 40 тисяч працівників, здебільшого в роздрібній торгівлі та закладах харчування. На пресконференції у Вінніпезі він зазначив, що родини досі відчувають подорожчання продуктів і оренди, а нова ставка зберігає баланс між зарплатами та цінами.

Торгова палата Манітоби (Manitoba Chambers of Commerce) заявила, що малий бізнес покриє ці витрати, але просить надалі повідомляти роботодавців про зміни завчасніше. Багато її членів і так платять більше за мінімум, щоб залучити працівників.

Ставка в Манітобі лишиться нижчою, ніж у Британській Колумбії, і вищою, ніж у Саскачевані. Роботодавці мають платити за новою ставкою за всі відпрацьовані години з 1 жовтня, зокрема студентам і тим, хто працює неповний день.

Judge: Accuracy: facts match the source. Minor distortion: "keeps wages in step with prices" became "зберігає баланс між зарплатами та цінами", which is slightly looser. "Покриє ці витрати" is acceptable for "absorb". Language: "платять більше за мінімум" is awkward, and "більше мінімуму" or "вище мінімуму" is better. "Пресконференція" should be "прес-конференція". "Повідомляти роботодавців" is a wrong government pattern, and "інформувати роботодавців" or "повідомляти роботодавцям" is better. "Мають платити за новою ставкою" is slightly clumsy. "Ставка зросте на 65 центів" repeats the lead idea. Usefulness: clear and complete, but there is no practical advice for readers, such as checking their pay stub. It also does not say what the previous rate was.

### rcmp-deepfake

**RCMP попереджає про любовні шахрайства з дипфейками в Метро-Ванкувері**

Канадська королівська кінна поліція (RCMP) застерігає мешканців Метро-Ванкувера від любовних афер, у яких шахраї видають себе за реальних людей за допомогою відео, створеного штучним інтелектом.

Цього року 85 мешканців регіону повідомили про втрати на загальну суму 2,3 млн доларів. Здебільшого аферист знайомиться з жертвою в застосунку для знайомств або в соцмережах, а потім влаштовує короткі відеодзвінки. Підроблені обличчя й голос роблять вигадану особу переконливою. Щойно жертва починає довіряти, шахрай просить гроші: на лікування, через заблокований рахунок або для вигідної інвестиції.

«Дзвінки виглядають справжніми, тому ці схеми так добре працюють», — каже сержантка відділу фінансових злочинів RCMP у Серрі (Surrey) Прія Сандху (Priya Sandhu).

Поліція називає тривожні ознаки: партнер не може зустрітися наживо, розмова раптово уривається, коли його просять повернути голову, а також будь-яке прохання про криптовалюту чи подарункові картки. Якщо гроші вже надіслано, одразу зверніться до банку, а потім повідомте місцеву поліцію та Канадський центр протидії шахрайству (Canadian Anti-Fraud Centre).

Judge: Accuracy: "so far this year" is rendered as "Цього року", which is acceptable. "Metro Vancouver residents reported losing" is fine. "У більшості випадків" became "Здебільшого аферист знайомиться", which is slightly awkward but faithful. "Medical emergency" became "на лікування", a minor shift in meaning. The source says "contact their bank immediately and report", and the post adds "а потім", which implies an order the source does not state. Minor. Language: the headline keeps "RCMP" in Latin script, while the glossary form is Канадська королівська кінна поліція (RCMP) on first mention, so the headline should arguably use the glossary form. "Метро-Ванкувері" is a clumsy form, and the body uses "Метро-Ванкувера", so the two are inconsistent. The headline's "любовні шахрайства з дипфейками" is a bit clunky. "Аферист/шахрай" is used interchangeably, which is fine. The Latin transliterations in brackets, (Surrey) and (Priya Sandhu), are somewhat padded. "Відділу фінансових злочинів RCMP у Серрі" is fine. The post has no "Що можна зробити" section, but the advice at the end is correct. Usefulness: clear and concise. It does not explain why this matters to Ukrainians in Canada, but it is relevant to residents of the region.

### ucc-mentorship

**В Едмонтоні запустили менторську програму для українців із CUAET**

Провінційна рада Конгресу українців Канади (КУК) в Альберті запустила в Едмонтоні менторську програму для українців, які приїхали до Канади за програмою CUAET.

Новоприбулим допомагатимуть 120 волонтерів-менторів. Здебільшого це українські канадці, що працюють у кваліфікованих робітничих професіях, медицині та інженерії. Ментор зустрічається зі своїм підопічним щонайменше двічі на місяць упродовж шести місяців. Він допомагає шукати роботу, визнавати кваліфікацію, орендувати житло та заповнювати урядові форми. Програму фінансує приватний фонд Prairie Bridges Foundation з Калгарі: він виділив 250 тисяч доларів на два роки.

Заявки від новоприбулих і від охочих стати менторами приймають до 15 січня. «Багато хто приїхав із сильним фахом, але не знає, як тут усе працює, а пояснити нікому. Ментор заощаджує місяці спроб і помилок», — каже координаторка програми Галина Мороз (Halyna Moroz). Наступного року рада планує поширити програму на Калгарі, якщо вистачить коштів.

Judge: Facts all match the source: 120 mentors, twice a month for six months, $250,000 over two years, Prairie Bridges Foundation in Calgary, January 15, Calgary expansion. Language problems: "урядові форми" is a calque, and "формуляри" or "бланки" would be more natural. "заощаджує місяці" is slightly stiff, and "економить" is more idiomatic. "кваліфікованих робітничих професіях" is a bit heavy for "trades". Usefulness: the post is clear and has no padding, but the application deadline is buried mid-paragraph, and the post says nothing about where or how to apply. That detail is missing from the source too, so the post could have said so or pointed to the UCC Alberta council.

### ircc-cuaet-pr

**Українці з CUAET зможуть отримати постійне резидентство: умови нової програми**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриє нову програму постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Прийом заявок розпочнеться 2 березня. Міністерство розгляне до 10 000 заявок. Охочі мають відпрацювати в Канаді щонайменше рік на повній зайнятості після приїзду за CUAET. Також потрібен результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. У заявку можна включити членів родини, які перебувають у Канаді. Тим, хто живе за межами Квебеку, також треба мати намір оселитися поза Квебеком: ця провінція сама добирає іммігрантів.

Конгрес українців Канади (Ukrainian Canadian Congress, КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхали понад 300 000 українців. За даними КУК, десятки тисяч із них досі мають тимчасовий статус.

Міністерство імміграції Канади оприлюднить посібник із подання заявки та перелік потрібних документів за два тижні до відкриття програми."

Judge: Accuracy: "Міністерство розгляне до 10 000 заявок" distorts the source, which says the pathway will accept up to 10,000 applications (a cap on intake, not on processing). "March 2" is given without the year, but the source doesn't give one either. "Відкриє нову програму" is not quite "pathway" (шлях), a minor wording issue. "Ukrainian Canadian Congress" is written as "Конгрес українців Канади (Ukrainian Canadian Congress, КУК)", which departs slightly from the glossary format "Конгрес українців Канади (КУК)". Language: "Охочі мають відпрацювати... на повній зайнятості" is slightly clumsy. "Добирає іммігрантів" is okay. "Поза Квебеком" is fine. The final paragraph has a stray closing quotation mark. Usefulness: the post is clear but has no "what to do" section. The last paragraph repeats "Міністерство імміграції Канади" instead of "IRCC", which is acceptable. The headline "зможуть отримати" slightly overpromises, since it is capped and conditional. The post does not say that applicants must have gained the year of work experience in Canada only after arriving under CUAET, although it comes close.

### statcan-population

**Населення Канади зросло лише на 0,2 % — найповільніше з 2020 року**

У третьому кварталі населення Канади збільшилося на 0,2 %. Для цього періоду це найнижчий приріст із 2020 року, повідомило в середу Статистичне управління Канади (Statistics Canada). Станом на 1 жовтня в країні проживали 41,7 млн людей.

Зростання майже повністю забезпечили нові постійні резиденти. Кількість тимчасових резидентів, серед яких іноземні студенти й тимчасові працівники, скоротилася на 65 тисяч. Це наслідок обмежень на видачу дозволів на навчання та змін у програмах тимчасової праці, які запровадили впродовж останніх двох років. Оттава заявляла, що хоче зменшити частку тимчасових резидентів у населенні.

Найшвидше серед провінцій зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст не сягнув і 0,1 %.

Економісти вважають, що повільніше зростання послабить тиск на ціни оренди у великих містах. Водночас у медицині та будівництві може загостритися нестача працівників.

Judge: Minor accuracy slips: the headline drops "for that period" (the source says slowest Q3 pace since 2020), so it reads as slowest overall since 2020. "Це наслідок" states a causal link more firmly than the source's "follows". "Announced" became "запровадили" (introduced). The language is clean and the glossary term is used correctly. Usefulness: the post is clear and concise but doesn't connect the news to Ukrainians in Canada, such as newcomers, students or workers on temporary status. It has no practical takeaway.

### akwesasne-policing

**Могавки й OPP підписали п'ятирічну угоду про поліцію на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про поліцейське обслуговування на 12 млн доларів. У понеділок про це повідомила рада.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й шосе поблизу громади, що лежить на перетині кордонів Онтаріо, Квебеку та штату Нью-Йорк. Частину коштів спрямують на новий відділок поліції на острові Корнволл (Cornwall Island) і на навчання восьми нових офіцерів. В OPP кажуть, що влітку патрулі зосередяться на контрабанді та безпеці на воді.

Верховна вождиня Лора Бенедикт (Laura Benedict) наголосила, що в громаді першими на виклики реагують поліцейські-могавки. «Наші офіцери знають ці води й ці родини. Угода дає їм ресурси для роботи», — сказала вона.

Judge: Accuracy: "Частину коштів" is a slight distortion, since the source says "the money will also pay for" the station and training, not only part of it. "OPP" is not expanded in the headline, and the glossary name appears only in the body. The source says the OPP said the patrols would focus on smuggling and boating safety "in the summer months", and the post renders this acceptably. "Mohawk Council of Akwesasne" is rendered as "Рада могавків Аквесасне", which is acceptable. "Могавки й OPP" in the headline is imprecise, because the signatories are the council and the OPP, not the Mohawk people. "Officers" as "офіцери" is slightly calqued; "поліцейські" would be more natural. "Що лежить на перетині кордонів" is fine. The post omits that the Mohawk police are described as first responders in the council's framing, though this is covered. The Ukrainian is mostly natural. "Мають" and "вождиня" are fine. "Поліцейське обслуговування" is slightly bureaucratic. Usefulness: the post says nothing about why this matters to Ukrainians in Canada, but it is a clear news summary with no padding. The "Верховна вождиня" translation of "Grand Chief" is acceptable.

### quebec-museum

**Музей сучасного мистецтва Монреаля відкривається після ремонту за 40 млн доларів**

Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal) у суботу знову відкриється для відвідувачів. Реконструкція його будівлі на Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Галерейна площа збільшилася на 2000 квадратних метрів. З'явилися новий вхід з боку вулиці Сент-Катрін і безкоштовна публічна тераса. Щопершої неділі місяця вхід до музею безкоштовний.

Першою в оновленому музеї показують виставку художниці Катерини Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а з 1998 року живе в Монреалі. На виставці 60 робіт, зокрема серія великих полотен, які Лисенко написала після поїздки до рідного міста 2023 року.

«Я хотіла, щоб люди бачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала художниця на попередньому показі в четвер. Виставка триватиме до 12 квітня.

Judge: Accuracy: the facts match the source. Two small points. "Added 2,000 m²" became "gallery space increased by 2,000 m²", which is fine. "Admission will be free on the first Sunday" became the present tense "is free", which is a slight shift but acceptable. The Ukrainian audience angle (Kharkiv) is kept.
Language: mostly natural. "Сент-Катрін" is an acceptable transliteration, though "Сент-Кетрін" is arguably closer to the Canadian pronunciation. "Катерина Лисенко" is a transliteration choice; the source gives the name only in English, so the Ukrainian form is guessed (Kateryna normally maps to Катерина). The headline "відкривається після ремонту" is slightly weak because the source describes a renovation or reconstruction; "ремонт" understates it. "Першою ... показують виставку" is slightly awkward; "Першою в оновленому музеї" is a minor stylistic quirk. "Галерейна площа" is a bit calque-like; "виставкова площа" would be better.
Usefulness: it is clear and concise and has no padding. It does not say that the Kharkiv link matters to Ukrainians in Canada. It also gives no practical details such as the address or ticket prices, though the source lacks them. The month of the opening date and year are missing from the source, so that is not the post's fault.

### cra-ccb-tips

**Без декларації виплати на дітей зупиняться в липні**

Агенція доходів Канади (CRA) нагадує родинам: щоб без перерви отримувати канадську допомогу на дітей (CCB), потрібно подати податкову декларацію до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку в липні переглядають за чистим доходом родини за попередній рік. Якщо агенція не має декларації кожного з батьків, виплати з липня припиняються, доки декларацію не подадуть і не опрацюють. Максимальна допомога на дитину до шести років зараз становить 8157 доларів на рік.

Що можна зробити:
• Не відкладайте декларацію на останній день: подайте її заздалегідь, щоб CRA встигла опрацювати її до липня.
• Нагадайте другому з батьків подати власну декларацію, навіть без доходу, — виплати залежать від обох.
• Якщо ви ще не оформили CCB, подайте заявку через особистий кабінет CRA My Account.
• За невисокого доходу зверніться до волонтерів безкоштовної податкової клініки у вашій громаді.

Failed checks: facts: missing: RC66; glossary: not used: номер соціального страхування (SIN)

Judge: Accuracy: the source says "2026 income tax return" (odd, but the post drops the year; it says "за попередній рік", which is fine). The post says "на дитину до шести років", which matches the source. "Максимальна допомога ... 8157 доларів" omits the "CRA says" attribution, but it is minor. The advice "file early so CRA can process before July" is general and safe. The "remind the other parent" advice is reasonable. The "apply via My Account" tip omits the SIN requirement, so it is slightly incomplete, and the RC66 mail option and the newcomer context are missing. Language: "допомога на дитину" is fine. "Розмір допомоги щороку в липні переглядають" is slightly awkward (impersonal plural). "Без декларації виплати на дітей зупиняться" is a bit imprecise as a headline, because it is the benefit that stops, not payments "for children", but it is acceptable. "кожного з батьків" is fine. "За невисокого доходу" is slightly bureaucratic. Usefulness: clear and concise. It does not mention the newcomer-specific steps (SIN, RC66/RC66SCH), which matter to this audience. The "доки... не опрацюють" is fine. The glossary is respected for CRA and CCB, though "CCB" is introduced as "канадську допомогу на дітей" and the post later uses "допомога на дитину".

### health-canada-recall-tips

**У Канаді відкликали три партії дитячої суміші Maple Meadow**

Міністерство охорони здоров'я Канади (Health Canada) закликає батьків припинити використання трьох партій сухої дитячої суміші Maple Meadow. Суміш може бути забруднена бактерією Cronobacter. Відкликані банки по 800 грамів продавали в продуктових магазинах та аптеках по всій країні. Термін придатності — червень 2027 року. Коди партій надруковані на денці банки. Про випадки захворювання не повідомляли.

Інфекція, яку спричиняє Cronobacter, трапляється рідко, але для немовлят може бути небезпечною. Найбільший ризик — для дітей, які народилися раніше строку, і малюків з ослабленим імунітетом. Ознаки хвороби: гарячка, погане годування, незвичний плач, сильна кволість.

Годувати дитину відкликаною сумішшю не можна. Її можна повернути до магазину, де купили, і отримати гроші назад. Якщо після суміші в дитини з'явилися симптоми, одразу зателефонуйте лікареві або на номер 811.

Що можна зробити:
• Знайдіть на денці банки код партії та термін придатності й порівняйте їх з даними у повідомленні про відкликання.
• Відкладіть банку окремо, щоб ніхто з родини не нагодував нею дитину, і візьміть її з собою до магазину.
• Перед дзвінком лікарю чи на номер 811 запишіть, коли дитина востаннє їла суміш і які симптоми з'явилися.
• Перш ніж купити іншу суміш, перевірте на сайті міністерства охорони здоров'я Канади (Health Canada), чи її не відкликали.

Judge: Accuracy: "Термін придатності — червень 2027 року" is slightly imprecise (best-before dates in June 2027, plural). The source never says the formula is sold "по всій країні" in the sense of stores nationwide—it does say "across Canada", so that is fine. The advice to compare the code with the recall notice is fine, but it doesn't say where the lot codes are listed, which makes it less useful. The last bullet, "check the Health Canada website", is generic and safe, with no invented specifics. Language: "дитячої суміші" is acceptable; "Термін придатності" for "best-before" is OK. "Погане годування" is a calque of "poor feeding" and should be "відмова від їжі / погано їсть". "Закликає ... припинити використання" is bureaucratic. "Про випадки захворювання не повідомляли" is acceptable but could be smoother. "Раніше строку" is better as "передчасно". "Зателефонуйте лікареві" is fine. Usefulness: the post is clear. The "Що можна зробити" list is somewhat padded: the first bullet is partly redundant, and the lot numbers are missing from the source, so the comparison cannot be done from the post itself.

