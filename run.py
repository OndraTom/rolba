import os
from scrapy.crawler import CrawlerProcess
from rolba.log import StandardOutputLogger
from rolba.configuration import Configuration, ConfigurationException
from rolba.record import VinylRecordFactory, VinylRecordDictMapper
from rolba.extraction import VinylEmpireRecordsExtractor, BlackVinylBazarRecordsExtractor
from rolba.repository import JsonFileRecordsRepository
from rolba.notification import EmailRecordsCollectionsNotifier
from rolba.email import SimpleSmtpEmailSender
from rolba.worker import WebSpiderExtractionsProcessor


logger = StandardOutputLogger()


try:
    configuration = Configuration(os.path.dirname(os.path.abspath(__file__)) + "/config.json")
    crawler_process = CrawlerProcess()

    WebSpiderExtractionsProcessor(
        crawler_process=crawler_process,
        records_collections_notifier=EmailRecordsCollectionsNotifier(
            email_sender=SimpleSmtpEmailSender(
                smtp_url=configuration.get_smtp_url(),
                user=configuration.get_emailing_user(),
                password=configuration.get_emailing_password()
            ),
            subscribers_emails=["o.tom@seznam.cz"],
            email_subject="Vinyl records notification"
        )
    ).register_extraction(
        title="Vinyl Empire",
        extractor=VinylEmpireRecordsExtractor(
            crawler_process=crawler_process
        ),
        repository=JsonFileRecordsRepository(
            file_path=os.path.dirname(os.path.abspath(__file__)) + "/storage/vinyl_empire_records.json",
            record_factory=VinylRecordFactory(),
            record_dict_mapper=VinylRecordDictMapper()
        )
    ).register_extraction(
        title="Black Vinyl Bazar",
        extractor=BlackVinylBazarRecordsExtractor(
            crawler_process=crawler_process
        ),
        repository=JsonFileRecordsRepository(
            file_path=os.path.dirname(os.path.abspath(__file__)) + "/storage/black_vinyl_bazar_records.json",
            record_factory=VinylRecordFactory(),
            record_dict_mapper=VinylRecordDictMapper()
        )
    ).run()
except ConfigurationException as e:
    logger.error(str(e))
    exit(1)
