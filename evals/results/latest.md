# Evaluation results

2026-11-28 · model `claude-sonnet-5-5` · prompts `cf1da8fc` · 9/9 posts written · **5/9 passed every check** · 45 Claude calls · $0.63 ($0.070 per post)

| Check | Pass rate |
| --- | --- |
| facts | 100% |
| glossary | 100% |
| people | 100% |
| names_kept | 100% |
| language | 100% |
| form | 89% |
| reviewer | 78% |

| Judge (1-5) | Average |
| --- | --- |
| accuracy | 4.00 |
| language | 4.00 |
| usefulness | 4.11 |

## Cases

| Case | facts | glossary | people | names_kept | language | form | reviewer | Judge (acc/lang/use) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| min-wage-mb | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| rcmp-deepfake | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 5/4/5 |
| ucc-mentorship | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/5/4 |
| ircc-cuaet-pr | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 4/4/4 |
| statcan-population | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | 4/4/4 |
| akwesasne-policing | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/3/4 |
| quebec-museum | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| cra-ccb-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | 4/4/4 |
| health-canada-recall-tips | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | 3/4/4 |

## Details

### min-wage-mb

**У Манітобі мінімальну зарплату підвищать до 16,50 долара**

Уряд Манітоби оголосив у вівторок, що з 1 жовтня мінімальна оплата праці в провінції становитиме 16,50 долара за годину. Це на 65 центів більше, ніж зараз.

Підвищення прив'язане до рівня інфляції в провінції, як цього вимагає закон, ухвалений 2023 року. За словами міністра праці Деніела Моро (Daniel Moreau), мінімальну зарплату отримують близько 40 тисяч працівників, здебільшого в роздрібній торгівлі та закладах харчування. «Родини й досі відчувають, як зросли ціни на продукти та оренду житла. Це підвищення зберігає відповідність між зарплатами та цінами», — сказав Моро на пресконференції у Вінніпезі.

Нову ставку роботодавці мають застосовувати до всіх відпрацьованих годин від 1 жовтня, зокрема для студентів і працівників на неповну ставку.

Торгово-промислова палата Манітоби (Manitoba Chambers of Commerce) каже, що малий бізнес упорається зі змінами, але просить у майбутньому повідомляти про них заздалегідь. За даними палати, багато її членів і так платять більше за мінімальну ставку, щоб залучити працівників.

Ставка в Манітобі залишається нижчою, ніж у Британській Колумбії, і вищою, ніж у Саскачевані.

Judge: Accuracy: the quote is a loose paraphrase, not a faithful translation ("Це підвищення зберігає відповідність" vs "keeps wages in step with prices"). "Small business would absorb the change" became "упорається зі змінами", which is a slight shift in meaning, since "absorb" implies bearing the cost. "Manitoba Chambers of Commerce" is rendered "Торгово-промислова палата Манітоби", which is acceptable but not exact. Language: "платять більше за мінімальну ставку" should be "платять більше, ніж мінімальна ставка" (calque/wrong construction). "мінімальну зарплату отримують" is fine. "Деніела Моро" has the English name in brackets, which is acceptable. "У майбутньому повідомляти заздалегідь" is a bit stiff, and "ніж зараз" is not in the source, though it is correct arithmetic only if the current rate is $15.85, so that part is inferred. Usefulness: clear and concise, but there is no explicit takeaway for readers, such as what it means for them as workers or employers, and the Saskatchewan and BC comparison is vague.

### rcmp-deepfake

**Дипфейк-шахраї в Метро-Ванкувері виманили 2,3 млн доларів**

Канадська королівська кінна поліція (RCMP) попереджає мешканців Метро-Ванкувера про романтичні шахрайства. Аферисти видають себе за реальних людей і для цього використовують відео, створене штучним інтелектом.

Цього року про втрати повідомили 85 осіб. Разом вони віддали шахраям 2,3 млн доларів. Здебільшого аферист знайомиться з жертвою в застосунку для знайомств або в соцмережах, а потім проводить короткі відеодзвінки. Дипфейк підміняє обличчя й голос, тому вигадана особа здається переконливою. Щойно з'являється довіра, починаються прохання про гроші: на лікування, через заблокований банківський рахунок або для вигідного вкладення. «Дзвінки виглядають справжніми, і саме тому ці схеми так добре працюють», — каже сержантка підрозділу фінансових злочинів RCMP у Серрі (Surrey) Прія Сандху (Priya Sandhu).

Поліція називає тривожні ознаки: співрозмовник не може зустрітися наживо, дзвінок раптово обривається, коли попросити повернути голову, а також будь-яке прохання про криптовалюту чи подарункові картки. Тим, хто вже переказав гроші, варто одразу зв'язатися з банком. Потім потрібно повідомити місцеву поліцію та Канадський антишахрайський центр (Canadian Anti-Fraud Centre).

Judge: Facts all match the source, and the glossary name is used correctly. Minor language points: "про втрати повідомили 85 осіб" is slightly clumsy (better: "85 осіб повідомили, що втратили гроші"). "Віддали шахраям" is a bit loose for "lost". "На лікування" narrows "medical emergency". The headline's "виманили" is a bit colloquial. The post is clear, has no padding, and gives the warning signs and what to do.

### ucc-mentorship

**В Едмонтоні запустили програму наставництва для українців, які приїхали за програмою CUAET**

Провінційна рада Конгресу українців Канади (КУК) в Альберті започаткувала в Едмонтоні програму наставництва для українців, які приїхали до Канади за програмою CUAET.

Кожному новоприбулому підберуть наставника серед 120 волонтерів. Здебільшого це канадці українського походження, які працюють у робітничих професіях, медицині та інженерії. Наставник зустрічається з підопічним щонайменше двічі на місяць упродовж шести місяців. Він допомагає шукати роботу, підтверджувати кваліфікацію, орендувати житло й заповнювати документи для державних установ.

Програму фінансує Prairie Bridges Foundation, приватний фонд із Калгарі. Він пообіцяв виділити на неї 250 тисяч доларів упродовж двох років.

«Багато хто приїхав із сильним фахом, але не знає, як тут усе працює, а підказати нікому, — каже координаторка програми Галина Мороз (Halyna Moroz). — Наставник заощаджує місяці спроб і помилок».

Заявки від новоприбулих і наставників приймають до 15 січня. Якщо дозволить фінансування, наступного року програму поширять і на Калгарі.

Judge: Accuracy: "Кожному новоприбулому підберуть наставника" slightly overstates the source, which says the program pairs newcomers with 120 mentors but does not promise every applicant a mentor. "Робітничі професії" is a loose rendering of "trades" (skilled trades). All numbers, names, the date and the funding are correct. Language: natural and clean, no real problems. Usefulness: clear on what the program is and who it is for, with the deadline. It does not say where or how to apply, but the source gives no details. The post is also somewhat bare on why it matters, apart from the quote.

### ircc-cuaet-pr

**Для українців із CUAET відкривається шлях до постійного резидентства**

Міністерство імміграції, біженців і громадянства Канади (IRCC) відкриває новий шлях до постійного резидентства (PR) для українців, які приїхали за програмою CUAET. Про це відомство повідомило в четвер.

Заявки почнуть приймати 2 березня, усього — до 10 000. Потрібно мати щонайменше рік повної зайнятості в Канаді, здобутий після приїзду за CUAET, і результат мовного тесту не нижче CLB 5 з англійської або NCLC 5 з французької. У заявку можна включити членів родини, які перебувають у Канаді. Тим, хто подається поза Квебеком, слід також планувати жити за межами цієї провінції: Квебек сам відбирає іммігрантів.

Конгрес українців Канади (КУК) привітав рішення, але вважає ліміт замалим. З 2022 року за CUAET приїхали понад 300 000 людей, і десятки тисяч із них досі мають тимчасовий статус. Міністерство імміграції Канади опублікує посібник із подання заявки та перелік документів за два тижні до відкриття.

Failed checks: reviewer: Твердження про «десятки тисяч» людей із тимчасовим статусом подано як факт. У джерелі це заява Конгресу українців Канади («the group says»), тому її треба прив'язати до КУК.; Незграбне формулювання «рік повної зайнятості... здобутий». У джерелі йдеться про досвід роботи на повну ставку (full-time work experience), тож краще написати «щонайменше рік досвіду роботи на повну ставку в Канаді, здобутого після приїзду за CUAET».

Judge: Accuracy: "More than 300,000 Ukrainians" became "понад 300 000 людей" (a small distortion, since the source says Ukrainians). "Повної зайнятості" is a slightly loose rendering of "full-time work experience", which would be "повний робочий день". The date "2 березня" is correct. The source says the pathway "will open", so "відкривається" in the headline is fine. Language: "здобутий після приїзду" is clumsy and ambiguous, because it sits after "в Канаді" and could attach to the wrong noun. "Ліміт замалим" is acceptable, though "замалий" is stiff; "занадто низький" is better. "Слід також планувати жити" is slightly awkward. The text is dense, with the requirements packed into one paragraph. "Посібник із подання заявки" is fine. Usefulness: it states what happened and why it matters. It has no practical next step, such as watching for the guide. It does not say that only one year of work after arriving counts, and it does not give the date the guide will be published (about 16 February), which is only implied.

### statcan-population

**Населення Канади зросло на 0,2 % — найменше для третього кварталу з 2020 року**

У третьому кварталі населення Канади збільшилося лише на 0,2 %. Для цього періоду це найнижчий приріст з 2020 року, повідомило в середу Статистичне управління Канади (Statistics Canada).

Станом на 1 жовтня в країні налічувалося 41,7 млн людей. Зростання майже повністю забезпечили ті, хто отримав постійне резидентство (PR). Кількість тимчасових резидентів, серед яких міжнародні студенти й тимчасові іноземні працівники, скоротилася на 65 тисяч.

Це сталося після того, як Оттава протягом останніх двох років обмежила видачу дозволів на навчання й змінила правила програм для тимчасових працівників. Федеральний уряд заявляв, що хоче зменшити частку тимчасових резидентів у населенні.

Серед провінцій найшвидше зростала Альберта — на 0,5 %. В Онтаріо та Британській Колумбії приріст не сягнув і 0,1 %.

Економісти вважають, що повільніше зростання послабить тиск на ринок оренди у великих містах, але може загострити дефіцит працівників у медицині й будівництві.

Failed checks: form: title too long

Judge: Accuracy: "non-permanent residents" rendered as "тимчасових резидентів" (acceptable, but source distinguishes); "Growth came from new permanent residents" rendered as "ті, хто отримав постійне резидентство" – fine. "Capped study permits and changed rules" is slightly stronger than "announced caps/changes" (implies already implemented) – minor slip. "Ontario and BC grew by less than 0.1%": rendered OK. Language: "Це сталося після того, як" is a bit clunky and implies sequence rather than the source's "follows"; "найнижчий приріст" fine; "на 0,2 %" with space is acceptable. "дефіцит працівників" is fine. Glossary: Statistics Canada used correctly; "постійне резидентство (PR)" used as per glossary. Usefulness: clear summary, but no explicit relevance for Ukrainians in Canada (e.g., those on temporary status); no what-to-do section, which isn't required. Headline repeats the lead somewhat.

### akwesasne-policing

**Поліція могавків і OPP підписали угоду на 12 млн доларів**

Рада могавків Аквесасне (Mohawk Council of Akwesasne) і Провінційна поліція Онтаріо (OPP) уклали п'ятирічну угоду про поліцейське обслуговування на 12 млн доларів. Про це рада повідомила в понеділок.

Поліцейська служба могавків Аквесасне (Akwesasne Mohawk Police Service) та OPP спільно патрулюватимуть річку й траси поблизу громади. Вона розташована на кордоні Онтаріо, Квебеку та штату Нью-Йорк. Кошти підуть також на новий поліцейський відділок на острові Корнволл (Cornwall Island) і на підготовку восьми нових поліцейських. За словами OPP, влітку патрулі зосередяться на боротьбі з контрабандою та на безпеці на воді.

Головна вождиня ради Лора Бенедикт (Laura Benedict) наголосила, що угода визнає поліцію могавків тими, хто першими реагує на виклики в громаді. «Наші офіцери знають ці води й ці родини. Тепер вони матимуть ресурси, щоб робити свою справу», — сказала вона.

Judge: Accuracy: "Тепер вони матимуть ресурси" slightly alters the quote ("This gives them the resources" – fine), but "траси" for highways is acceptable. Minor: the OPP attribution of summer focus is correct. "Вона розташована на кордоні" – source says it straddles the borders of Ontario, Quebec and NY; fine. Minor drift: "Mohawk Council of Akwesasne" rendered as "Рада могавків Аквесасне" OK. The statement "the council said Monday" kept. Language: "Поліція могавків" in headline is vague/ambiguous (the service is the Akwesasne Mohawk Police Service); "Вона розташована" is ambiguous after "поблизу громади" (could refer to river/highways); "поліцейське обслуговування" is a calque of "policing"; "угода про поліцейське обслуговування" is stilted; "тими, хто першими реагує на виклики" is awkward English-like structure (should be "першими реагують"); "Головна вождиня" for Grand Chief is questionable (ordinarily "велика вождиня"/"ґранд-вождиня"); "офіцери" for officers is a calque, "поліцейські" better; "робити свою справу" a bit calqued. Usefulness: conveys what happened but doesn't explain relevance to Ukrainians in Canada, and the structure puts the quote last with the order of facts slightly rearranged; no padding. Source says the community "straddles" Ontario, Quebec and NY; the post's "на кордоні" is okay. Source says "river and highways near the community" – fine.

### quebec-museum

**Музей сучасного мистецтва в Монреалі відкрився після реконструкції за 40 млн доларів**

Музей сучасного мистецтва Монреаля (Musée d'art contemporain de Montréal) у суботу знову приймає відвідувачів. Реконструкція будівлі в комплексі Place des Arts тривала чотири роки й коштувала 40 млн доларів.

Галереї стали більшими на 2000 квадратних метрів. З'явилися новий вхід з вулиці Сент-Катрін і безкоштовна тераса для всіх охочих. У першу неділю кожного місяця вхід до музею вільний.

Першу виставку присвятили художниці Катерині Лисенко (Kateryna Lysenko). Вона народилася в Харкові, а з 1998 року живе в Монреалі. У залах показують 60 робіт, серед них серію великих полотен, які вона написала після поїздки до рідного міста 2023 року. Виставка триватиме до 12 квітня.

«Я хотіла, щоб люди бачили Харків як місто світла, студентів і музики, а не лише як місце з новин», — сказала Лисенко на передпоказі.

Judge: Accuracy: the headline and lead say the museum "reopened", but the source says it reopens on Saturday, so the tense is slightly off. The lead uses "у суботу знову приймає", which is fine. The source says "$40-million" without naming a currency, and the post assumes dollars; this is a minor point. "Вхід вільний" is fine. The lead does not say the preview was on Thursday, but that is not an error. Language: "Галереї стали більшими на 2000 квадратних метрів" is slightly awkward, because the source says space was added, so "додалося 2000 кв. м" would be better. "Сент-Катрін" is acceptable. "Першу виставку присвятили" is acceptable. Usefulness: the post is clear and has no padding. It does not mention that the first-Sunday admission is free for everyone, and it gives no practical details such as the address or opening hours, though the source has none. It also does not say why the Kharkiv-born artist's show matters to Ukrainians, though the quote helps.

### cra-ccb-tips

**Без податкової декларації допомогу на дітей перестануть виплачувати**

Агенція доходів Канади (Canada Revenue Agency, CRA) нагадує: щоб без перерв отримувати канадську допомогу на дітей (Canada Child Benefit, CCB), потрібно подати податкову декларацію за 2026 рік до 30 квітня. Це стосується й тих, хто торік не мав доходу.

Розмір допомоги щороку в липні перераховують за чистим доходом сім'ї за попередній рік. Якщо в CRA немає декларації когось із батьків, виплати з липня припиняють, доки декларацію не подадуть і не опрацюють. Максимальна допомога на дитину до шести років зараз становить 8157 доларів на рік.

Що можна зробити:
• Домовтеся з чоловіком чи дружиною, щоб кожен подав власну декларацію до 30 квітня, навіть без доходу.
• Якщо ви нещодавно приїхали й ще не оформили CCB, подайте заяву через CRA My Account після отримання номера соціального страхування (SIN).
• Можна подати заяву поштою: заповніть форми RC66 і RC66SCH. У RC66SCH запитують про статус проживання в Канаді та доходи за її межами.
• Якщо дохід невисокий, подайте декларацію безкоштовно через громадські волонтерські податкові клініки (community volunteer tax clinics).

Judge: Accuracy: "2026 income tax return... even if no income last year" is consistent with the source. Minor slip: "Максимальна допомога на дитину" — source says maximum benefit for a child under six, ok; "зараз" matches "now". The source says "payments stop in July" for missing return of both parents; the post says "когось із батьків" (either parent), which distorts "both parents" wording — a minor distortion. Headline "перестануть виплачувати" is stronger than the source: payments only pause until filing, not permanently. Language: glossary form "канадська допомога на дітей" was not used exactly on first mention (headline uses "допомогу на дітей", body uses "канадську допомогу на дітей" — fine, but "допомога на дитину" later is a variation). "Домовтеся з чоловіком чи дружиною" is a bit awkward; "подати заяву через CRA My Account" fine. "Порядок: подайте заяву поштою" is okay. Usefulness: clear, actionable; slightly repeats the April 30 deadline and the newcomer steps are split across two bullets.

### health-canada-recall-tips

**Maple Meadow відкликає три партії дитячої суміші через ризик Cronobacter**

Міністерство охорони здоров'я Канади (Health Canada) просить батьків припинити використовувати три партії сухої дитячої суміші Maple Meadow. Вони можуть бути заражені бактерією Cronobacter. Йдеться про банки по 800 грамів із терміном придатності до червня 2027 року. Їх продавали в продуктових магазинах і аптеках по всій країні. Коди партій надруковані на денці банки.

Про випадки захворювання не повідомляли. Інфекція Cronobacter трапляється рідко, але може бути небезпечною для новонароджених, особливо недоношених або з ослабленим імунітетом. Її симптоми: гарячка, поганий апетит, незвичний плач і сильна млявість.

Годувати дітей відкликаною сумішшю не можна. Її слід повернути в магазин, де купили, і отримати гроші назад. Якщо після такої суміші в дитини з'явилися симптоми, негайно зверніться до лікаря або зателефонуйте на номер 811.

Що можна зробити:
• Перегляньте вдома банки Maple Meadow по 800 г із терміном придатності до червня 2027 року й звірте код партії на денці з повідомленням про відкликання.
• Відкладіть відкликану банку окремо від іншої дитячої їжі, щоб ніхто нею не скористався, доки не віднесете її до магазину.
• Якщо дитина вже пила суміш із відкликаної партії, стежте за її самопочуттям і за перших ознак хвороби зверніться до лікаря або на 811.
• Не переливайте суміш в інший контейнер: так буде важко звірити партію й термін придатності.

Failed checks: reviewer: «із терміном придатності до червня 2027 року» — у джерелі best-before dates in June 2027, тобто дати «найкраще вжити до» припадають на червень 2027 року. «До червня» означає раніше за червень, а «термін придатності» — це не best-before. Треба: «з датою «найкраще вжити до» в червні 2027 року».; Заголовок стверджує, що відкликання робить компанія Maple Meadow. У джерелі про це не сказано: там лише Health Canada радить батькам не використовувати продукт. Головним суб'єктом краще вказати Health Canada або сформулювати безособово.

Judge: Accuracy: "best-before dates in June 2027" is rendered as "термін придатності до червня 2027" — "до червня" is ambiguous (could mean before June) and "термін придатності" is slightly off from "best before" (the source says dates are in June 2027), a minor slip. "Cronobacter infection" handled fine. The first mention uses the glossary form, but with a lowercase "Міністерство", whereas the glossary has lowercase "міністерство" (minor). "Заражені" is ok for "contaminated", though "забруднені/інфіковані" would be more precise. "Звірте з повідомленням про відкликання" refers to a notice with lot codes not given in the source; acceptable general advice. "Поганий апетит" for "poor feeding" is a bit loose. "Гроші назад" is colloquial; "відшкодування" would be better. The "Що можна зробити" list is mostly sensible and safe; the last bullet (don't transfer to another container) is reasonable. The list partly repeats the body text (symptoms/811, check cans), which adds some padding. Also "по всій країні" is fine. The headline attributes the recall to Maple Meadow ("відкликає"), whereas the source says Health Canada recalls it — slight distortion of the actor.

