from typing import List
from datetime import datetime
import json
from loguru import logger

from motor.motor_asyncio import AsyncIOMotorDatabase
from wiki_service.db.migrations.migration import Migration
from wiki_service.db.entry_repository import EntryRepository
from wiki_service.models.wikiEntry import WikiEntry

class InitialEntries(Migration):

    def timestamp(self) -> datetime:
        return datetime.fromisoformat('2022-06-29T12:40:00')

    async def migrate(self, db: AsyncIOMotorDatabase) -> None:
        await db.articles.insert_many(list(map(lambda x: x.dict(), self.data())))

    def data(self) -> List[WikiEntry]:
        try:
            parsed = json.loads(JSON_DATA)
        except json.JSONDecodeError as e:
            logger.exception('Invalid data in migration {} (Error: {})', __name__, e)
            return []
        
        entries: List[WikiEntry] = []
        for obj in parsed.values():
            logger.debug('Parsed article {}', obj)
            entries.append(WikiEntry(**obj))

        return entries


JSON_DATA = r"""
{
  "ABCModell": {
    "title": "ABC Modell",
    "content": "\n\nAnhand der ABC - Eselsbrücke lässt sich die Entstehung von Gefühlen veranschaulichen:\n\nA steht für eine auslösende Situation, B für die Bewertung der Situation und C für das englische Wort *consequence*. Ein Beispiel für eine auslösende Situation könnte sein, dass der Bus zu spät kommt. Diese Situation könnte negativ bewertet werden, weil man später zuhause ankommt oder aber man findet es vielleicht gar nicht so schlecht, weil man gerade noch mit seinen Freunden am Quatschen ist. Aus der jeweiligen Bewertung resultiert dann *in consequence ein* spezielles Gefühl. In unserem Beispiel könnte man sich über die Verspätung ärgern oder freuen.Je nachdem können also bei der gleichen auslösenden Situation (A) aufgrund von unterschiedlicher Bewertung (B) sehr unterschiedliche Gefühle die Konsequenz (C) sein.\n",
    "basename": "ABCModell"
  },
  "ALPENMethode": {
    "title": "ALPEN-Methode",
    "content": "\n\nDie ALPEN-Methode gibt dir eine Struktur um einen Tagesplan zu erstellen, wenn du einmal das Gefühl hast, dass du gar nicht mehr weißt wo du anfangen sollst. Das Wort ALPEN sind dabei die Anfangsbuchstaben der einzelnen Schritte, die du nach und nach durch gehst.\n\nDas „A“ steht für „Aufgaben notieren“: Dabei schreibst du dir auf, was du dir an diesem oder am nächsten Tag vornimmst. Die Aufgaben können sowohl Schulaufgaben als auch Hobbies oder andere Dinge sein, die du machen möchtest. Weiterhin priorisierst du deine zuvor aufgeschriebenen Aufgaben. Was ist wichtig und was ist eher unwichtig?\n\nIm nächsten Schritt, dem „L“ schätzt du die Länge der einzelnen Aufgaben ein: Wie lange brauche ich für jede einzelne Aufgabe? Wann muss ich damit fertig sein?\n\nDas „P“ steht für „Pufferzeiten einplanen“: Dieser nächste Schritt ist wichtig, weil die geschätzte Länge nie ganz genau stimmt und du dir deshalb gleich schon einen Zeitpuffer einplanen solltest. Als Faustregel kannst du dir merken, dass du dir etwa ein Drittel des geschätzten Zeitaufwandes für eine Aufgabe noch zusätzlich als Reserve einplanen solltest.\n\nNun heißt es „Entscheidungen zu treffen“: Dies ist der Schritt „E“ in der ALPEN-Methode. Entscheide dich welche Aufgabe du zuerst erledigen möchtest. Du solltest mit der wichtigsten beziehungsweise dringendsten Aufgabe beginnen und dann mit der Zweitwichtigsten fortfahren und so weiter! Es kann an einigen Tagen auch vorkommen, dass du nicht alle Aufgaben schaffst. Das ist vollkommen okay und passiert auch den strukturiertesten Menschen einmal. Durch den Schritt „Entscheidungen treffen“ hast du aber selbst in diesem Falle die wichtigsten Dinge gleich als erstes abgearbeitet. Die weniger wichtigen Aufgaben, können dann auch bis morgen warten.\n\nDer letzte Schritt „N“ ist die „Nachkontrolle”: Das heißt am Ende des Tages kontrollierst du welche Aufgaben du geschafft hast und welche noch anstehen. Dies ist ein guter Zeitpunkt dir gleich Aufgaben für den nächsten Tag zu notieren und somit die ALPEN-Methode von vorne zu beginnen.\n",
    "basename": "ALPENMethode"
  },
  "Atemuebungen": {
    "title": "Atemübung",
    "content": "\n\nWenn du dich gestresst fühlst, können Atemübungen helfen akute Stresssymptome zu minimieren. Wenn wir gestresst sind, vergessen wir manchmal lange genug auszuatmen. Weiterhin können Atemübungen dabei helfen sich zu entspannen, Gedanken abzuschalten und loszulassen.\n\nEine mögliche Atemübung ist folgende:\nMache es dir auf deinem Stuhl gemütlich, atme tief ein und aus und schließe deine Augen oder schaue auf den Boden. Atme nun bewusst ein und zähle dabei in Gedanken bis Vier (1-2-3-4). Halte deinen Atem nun vier Sekunden lang (1-2-3-4). Atme dann aus und zähle dabei bis 8 (1-2-3-4-5-6-7-8). Diesen Ablauf kannst du mehrmals wiederholen.\n",
    "basename": "Atemuebungen"
  },
  "Emolutionsregulation": {
    "title": "Emotionsregulation",
    "content": "\n\nGefühle geben uns wichtige Informationen darüber was wir gerade brauchen (Bei Traurigkeit brauchen wir zum Beispiel Unterstützung oder Trost; Bei Wut müssen wir einen Konflikt klären etc.). Dementsprechend können also auch negative Emotionen nützlich sein. Damit es uns gut geht und wir in unserer Umwelt und mit anderen Menschen zurechtkommen, kann es allerdings auch notwendig und sinnvoll sein, unsere Gefühle etwas und in die eine oder andere Richtung zu beeinflussen. Generell versuchen wir positive Emotionen zu fördern und negativen Emotionen entgegenzuwirken. Aber vielleicht habt ihr auch schonmal eure Freude über einen eigenen Erfolg ein Stück weit zurückgehalten, weil ein/e Freund/in von euch eben im Gegensatz zu euch nicht so eine gute Note bekommen hat und ihr es ihm/ihr jetzt nicht direkt auf die Nase binden wolltet. Zur Emotionsregulation kannst du an verschiedenen Punkten ansetzen, die du auch schon aus dem ABC-Modell (siehe ABC-Modell) kennst: Zum Beispiel kannst du versuchen auslösende Situationen auszuwählen, die positive Emotionen fördern (Situationsauswahl) oder eine Situation zum besseren verändern (Situationsmodifikation). Genauso kannst du an der Bewertung arbeiten (Ist etwas wirklich wichtig, so schlimm, Umwidmungen, andere Perspektive, das Positive sehen) oder versuchen, das Gefühl direkt anzugehen (Kurzfristige Unterdrückung, es auf eine sichere Art und Weise rauslassen etc).\n\nEmotionsregulation= Wissen und Verhalten um angenehme Gefühle zu fördern und unangenehmen Gefühlen vorzubeugen und entgegenzuwirken, um möglichst adaptiv und funktional mit sich, seinen Emotionen und der Umwelt umgehen zu können.\n",
    "basename": "Emolutionsregulation"
  },
  "Emotionen": {
    "title": "Emotion",
    "content": "\n\nUnterschiedliche Emotionen wie Wut, Angst, Freude, Trauer oder Überraschung entstehen in Reaktion auf verschiedene auslösende Situationen und wie wir diese Situationen bewerten (siehe ABC-Modell). Man kann sie sich als vorbereitete Antwort-Tendenzen vorstellen, die uns im Laufe der Evolution geholfen haben rasch und möglichst adaptiv auf wichtige Chancen und Herausforderungen in unserer Umwelt zu reagieren: Beispielsweise indem unser Körper und Gehirn automatisch das Emotions-Programm ‚Angst‘ abruft, welches uns fluchtbereit macht, ohne dass wir dafür groß nachdenken müssten.. Jede Emotion besteht dabei aus vier miteinander in Wechselwirkung stehenden Elementen: Der die Emotion begleitenden Körperreaktion (1), den damit einhergehenden Gedanken (2), dem dazugehörigen Gefühl (3) und daran anschließendes Verhalten (4). Wenn man also eine Emotion beeinflussen will (siehe Emotionsregulation), um zum Beispiel einer negativen Emotion entgegenzuwirken, kann man an diesen vier Stellschrauben ansetzen.\n",
    "basename": "Emotionen"
  },
  "Entstigmatisierung": {
    "title": "Entstigmatisierung",
    "content": "\n\n*Normalisierung* psychischer Probleme als etwas, was viele Menschen erleben und eine Person nicht besser oder schlechter macht. Dadurch sollen sich Menschen eher trauen offen mit psychischen Problemthemen umzugehen und sich gegebenenfalls nötige Unterstützung und professionelle Hilfe zu suchen.\n",
    "basename": "Entstigmatisierung"
  },
  "Faehigkeiten_Kompenzvermittlung": {
    "title": "Fähigkeiten-/Kompetenzvermittlung",
    "content": "\n\nWerkzeugkasten an Knowhow und unterschiedlichen Übungen kann einen Menschen in die Lage versetzen besser mit belastenden Situationen umzugehen und Selbstfürsorge zu betreiben. Dadurch soll es erst gar nicht zu größeren Krisen und psychischen Störungen kommen.\n",
    "basename": "Faehigkeiten_Kompenzvermittlung"
  },
  "Fassmodell": {
    "title": "Fassmodell",
    "content": "\n\nDas Fassmodell ist eine Metapher für unsere persönliche Belastungsgrenze. Es füllt sich mit Dingen, die uns Kraft kosten und belasten, zum Beispiel Stress, Anforderungen, negativen Gefühlen und Krankheit. Diese Faktoren lassen sich in soziale (Streit, Erwartungen andere), biologische (Gene, Krankheit, Zyklus, Hormonspiegel) und psychologische Faktoren (Stress, Werte, Selbstwert, Bedürfnisse) unterteilen. Dabei kann unser Geist mit diesen Belastungen in Maßen gut umgehen, bis es irgendwann mal zu viel auf einmal wird und das Fass “überläuft”. Wie dieses Überlaufen aussieht unterscheidet sich von Person zu Person und kann auch von Situation zu Situation unterschiedlich sein. Manche merken es zum Beispiel,  dass ihnen gerade alles zu viel ist, wenn sie aggressiv reagieren oder sie sich am liebsten “die Decke über den Kopf ziehen” würden. Auch wann genau das Fass überläuft ist bei jedem unterschiedlich, da alle unterschiedliche Voraussetzungen haben. Emotionsregulation (Siehe Emotionsregulation) und unsere Ressourcen können uns dabei helfen, dass das Fass nicht überläuft beziehungsweise es auch wieder zu leeren, indem wir zum Beispiel positive Aktivitäten einplanen und unsere Aufmerksamkeit gezielt lenken.\n",
    "basename": "Fassmodell"
  },
  "MentaleGesundheit": {
    "title": "Mentale Gesundheit",
    "content": "\n\nMentale Gesundheit ist nicht nur die Abwesenheit von Krankheit, sondern umfasst auch Dinge wie Wohlbefinden, das Ausschöpfen eigener Fähigkeiten, sowie Belastungen bewältigen zu können und sich selbst zu verwirklichen. Mentale Gesundheit  ermöglicht so ein kreatives und produktives Leben, gesellschaftliche Teilhabe und versetzt uns in die Lage mit anderen beiderseitig zufriedenstellende Beziehungen einzugehen - sich aber auch wohl fühlen zu können, wenn man alleine ist.\n",
    "basename": "MentaleGesundheit"
  },
  "Problembewusstsein": {
    "title": "Problembewusstsein",
    "content": "\n\nDie Sensibilisierung für und Auseinandersetzung mit dem Thema mentale Gesundheit schafft ein Bewusstsein für eventuelle Belastungen und psychische Probleme. Das ist der erste Schritt, um diese auch aktiv angehen und bewältigen zu können.\n",
    "basename": "Problembewusstsein"
  },
  "Psyche": {
    "title": "Psyche",
    "content": "\n\nDie Gesamtheit des menschlichen Fühlens, Empfindens & Denkens.\n",
    "basename": "Psyche"
  },
  "Psychologie": {
    "title": "Psychologie",
    "content": "\n\nDas Wort Psychologie leitet sich von den zwei griechischen Wörtern *psyche* (= Seele) und *logos* (= Kunde oder Lehre) ab und bedeutet übersetzt so viel wie „Seelenkunde“.\n\nPsychologie ist die Wissenschaft vom Erleben und Verhalten des Menschen. Das bedeutet, dass durch wissenschaftliche Methoden die Gefühle, die Wahrnehmung und das Verhalten von Menschen untersucht wird, um dadurch Rückschlüsse auf innere Vorgänge des Menschen zu ziehen. Fragen wie „Warum verhält sich der Mensch in dieser Situation so wie er es tut? oder „Warum verhalten sich zwei Menschen in der gleichen Situation unterschiedlich?“ könnten psychologische Forschungsfragen darstellen. In der Forschung wird dabei versucht Verhalten zu beobachten, zu erklären und vorherzusagen.  \n\nDie Psychologie hat viele verschiedene Teilgebiete: Darunter sind zum Beispiel die Schulpsychologie (Unterstützung von Schüler:innen und Lehrkräften zum Thema Lernen, Verhalten und Bewältigung von Krisen im schulischen Kontext), Wirtschaftspsychologie (Anwendung von psychologischen Theorien im wirtschaftlichen Kontext, wie zum Beispiel in der Werbung oder Produktentwicklung) und klinische Psychologie (Erforschung der Ursache und Behandlung psychischer Krankheiten).\n",
    "basename": "Psychologie"
  },
  "Psychotherapie": {
    "title": "Psychotherapie",
    "content": "\n\nPsychotherapie ist ein Anwendungsgebiet der klinischen Psychologie. Das Wort Psychotherapie leitet sich von zwei griechischen Wörtern ab und bedeutet so viel wie „Behandlung der Seele“. Die Psychotherapie kommt immer dann ins Spiel, wenn es einer Person mental über einen längeren Zeitraum nicht gut geht. Die Psychotherapie wird von einem ausgebildeten Psychotherapeuten oder einer Psychotherapeutin mit dem Klienten oder der Klientin durchgeführt. Dabei wird unter anderem versucht herauszufinden was genau das Problem ist und wo die Ursache des Problems liegt. Weiterhin wird mit dem Klienten oder der Klientin versucht einen Weg zu finden das Problem zu lösen, sodass raschere Besserung eintreten kann.\n",
    "basename": "Psychotherapie"
  },
  "Selbstwirksamkeit": {
    "title": "Selbstwirksamkeit",
    "content": "\n\nStärkung des (Selbst-)Vertrauens, dass man Situationen und Herausforderungen erfolgreich und auch aus eigener Kraft bewältigen kann. Dieses Vertrauen ist Voraussetzung dafür, dass man diese Herausforderungen überhaupt erst angeht.\n",
    "basename": "Selbstwirksamkeit"
  },
  "Selfcare": {
    "title": "Selfcare",
    "content": "\n\nDas Wort *Selfcare* setzt sich aus den zwei englischen Wörtern „self“ (= selbst) und „care“ (=sich um jemanden kümmern) zusammen. Übersetzt heißt es also so viel wie “Sich um sich selbst kümmern“. Der deutsche Fachbegriff lautet “Selbstfürsorge”.\n\nWir sind unseren Gefühlen nicht hilflos ausgeliefert, sondern können Einfluss auf diese haben. Um für unser mentales Wohlbefinden zu sorgen, also uns gut zu fühlen, können wir *Selfcare* betreiben.\n\nEs gibt verschiedene Strategien für *Selfcare*, die du ausprobieren kannst. Dazu gehören zum Beispiel: Meditation, Atemübungen und das Einplanen von Pausen (siehe Atemübung). Dennoch ist *Selfcare* etwas sehr Individuelles. Du musst selbst durch Ausprobieren herausfinden, welche Selfcare-Strategien für dich funktionieren. Dabei kannst du kreativ und individuell werden, solange es dir gelingt durch diese Strategie dein mentales Wohlbefinden ein wenig zu verbessern. Die Strategie, die für eine andere Person funktioniert, muss nicht unbedingt für deine Selbstfürsorge funktionieren.\n",
    "basename": "Selfcare"
  },
  "Sicherheitsnetz": {
    "title": "Sicherheitsnetz",
    "content": "\n\nDas Sicherheitsnetz ist eine Metapher, die dir dabei helfen kann, zu überlegen wer oder was dich auffängt, wenn es dir einmal nicht so gut geht. Dein Sicherheitsnetz setzt sich aus verschiedenen Faktoren zusammen. Gemeint sind Menschen, Dinge und Aktivitäten, die dir Kraft geben und dir gut tun. Wenn es uns einmal nicht so gut geht, fällt es uns oft schwer effektiv darüber nachzudenken was uns in diesem Moment gut tun würde. In genau diesem Moment hilft es, wenn du dir vorher schon Gedanken darüber gemacht hast, wer oder was dir gerade helfen würde. Das Sicherheitsnetz ist ein bildlicher Weg dir bewusst zu machen wer oder was dich im Hintergrund stärkt.\n",
    "basename": "Sicherheitsnetz"
  },
  "Stress": {
    "title": "Stress",
    "content": "\n\nStress ist ein Spannungszustand, der unseren Körper bereit für eine Reaktion macht. In diesem Zustand sind wir in Alarmbereitschaft und können auf eine potenzielle Gefahr schneller reagieren. Die körperliche Reaktion, die eine Stresssituation aus löst, ermöglicht es uns in den *Fight or Flight* - Modus zu schalten. Dafür werden Energiereserven des Körpers genutzt. Dies könnte zum Beispiel dafür sorgen, dass wir uns in einer Prüfungssituation über einen längeren Zeitraum gut konzentrieren können.\n\nProblematisch wird es, wenn der Stress chronisch und lang anhaltend ist: Das kann uns sowohl körperlich als auch psychisch überfordern und im schlimmsten Fall in Krankheit enden.\n\nAlle Faktoren, die Stress auslösen, nennt man Stressoren. Stressoren sind ganz unterschiedliche Faktoren wie zum Beispiel Müdigkeit, Hitze oder Überforderung. Wie stark die Einwirkungen eines Stressors auf einen Menschen ist, ist individuell unterschiedlich. Ob eine Situation oder ein Stressor in mir Stress auslöst, ist auch abhängig vom Füllstand meines Fasses (siehe Wiki-Eintrag Fassmodell).\n\nIn stressigen Situationen kann es helfen auf dich selber zu achten, also *Selfcare* zu betreiben (siehe Selfcare) und zum Beispiel Atemübungen oder andere Achtsamkeitsübungen auszuprobieren (siehe Atemübung).\n",
    "basename": "Stress"
  },
  "Wut": {
    "title": "Wut",
    "content": "\n\nWut ist eine der 7 Basisemotionen, die von dem Psychologen Paul Ekman erforscht worden sind. Das bedeutet, dass Wut eine jener Emotionen ist, die jedem Menschen angeboren sind. Die Emotion Wut kann dadurch umschrieben werden, dass es sich um das Erleben von Ärger in einer intensiveren Form handelt, welches gleichzeitig mit Impulsen verknüpft ist aggressiv zu handeln.\n\nIn der Entwicklungsgeschichte des Menschen dient die Emotion Wut zum Beispiel zur Verteidigung des eigenen Lebensraumes.\n\nWut entsteht durch Frustration oder das Erleben von Situationen gegen die eine Abneigung besteht.\n",
    "basename": "Wut"
  }
}
"""
