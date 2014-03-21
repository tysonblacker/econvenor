from meetings.models import DistributionRecord


def find_or_create_distribution_record(group, meeting, doc_type):
    """
    Finds the distribution record for a document, or creates a blank
    one if none exists. Returns the distribution record.
    """
    try:
        record = DistributionRecord.objects.get(group=group, meeting=meeting, 
                                                doc_type=doc_type)
    except DistributionRecord.DoesNotExist:
        record = DistributionRecord(group=group,
                                    meeting=meeting,
                                    doc_type=doc_type,
                                    )
        record.save(group)
    
    return record
