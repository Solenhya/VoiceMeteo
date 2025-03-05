import VoiceMeteo.app.services.NerTransform as NerTransform
import pytest

@pytest.mark.integration
@pytest.mark.parametrize("textEntrer , infoExtraite",[
    ("Bonjour je suis a Tours demain",{"date":["demain"],"loc":["Tours"]}),
    ("Quel est la météo a Lyon dans deux jours",{"date":["dans deux jours"],"loc":["Lyon"]})
])
def testNer(textEntrer,infoExtraite):
    retour = NerTransform.GetInfoAll(textEntrer)
    assert retour == infoExtraite