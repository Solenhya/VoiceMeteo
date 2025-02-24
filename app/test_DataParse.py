import dataParse
import datetime
import pytest
import dateparser

@pytest.fixture
def sample_single():
    return {"date":["24 Decembre 2017"],
            "loc":["Tours"]}

@pytest.fixture
def sample_range():
    return {"date":["vendredi a samedi"],"loc":["Tours"]}

@pytest.fixture
def result_range():
    return{"date":[dateparser.parse("vendredi",settings={'PREFER_DATES_FROM': 'future'}),dateparser.parse("samedi",settings={'PREFER_DATES_FROM': 'future'})],"latitude":47.395476,"longitude":0.694273}

@pytest.mark.integration
@pytest.mark.parametrize("listeDate,min,max",
                         [
                             ([datetime.datetime()])
                         ])


@pytest.mark.integration
@pytest.mark.parametrize("info_range , expected_return_range", 
                        [
                                (
                                 {"date":["vendredi a samedi"],"loc":["Tours"]} ,
                                 {
                                        "date":[dateparser.parse("vendredi",settings={'PREFER_DATES_FROM': 'future'}),
                                                dateparser.parse("samedi",settings={'PREFER_DATES_FROM': 'future'})],
                                        "loc":[{"latitude":47.395476,"longitude":0.694273}],
                                        "status":"Success"
                                  }
                                ),
                                (
                                    {"date":["vendredi"],"loc":[]},
                                    {
                                        "date":[dateparser.parse("vendredi",settings={'PREFER_DATES_FROM': 'future'})],
                                        "loc":[],
                                        "status":"ErLoc"
                                    }
                                ),
                                (
                                    {"date":[],"loc":[]},
                                    {
                                        "date":[],"loc":[],"status":"ErDate/ErLoc"
                                    }
                                )
                        ])
def testMultipleParam(info_range,expected_return_range):
    retour = dataParse.parseAll(info_range)
    assert retour == expected_return_range

def testsingleDataExtra(sample_single):
    info = sample_single
    retour = dataParse.parseSingleData(info)
    assert retour["date"]== datetime.datetime(2017, 12, 24, 0, 0)
    assert retour["loc"]["latitude"]==47.395476
    assert retour["loc"]["longitude"]==0.694273
