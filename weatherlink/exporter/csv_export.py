#!/usr/bin/false

import csv


class CSVOutput(object):
    def __init__(self, filename, fields):
        self.filename = filename
        self.f = open(self.filename, 'a+b')
        self.fields = fields

    def initCSV(self):
        """
        make sure that the CSV file has the appropriate headers -- if they
        are missing, then write them, if they do not match up with
        the user's specified fields then output a warning message. Finally,
        return date and time of the most recent record as a
        datetime.datetime object (or None if there are no records).
        """
        reader = csv.reader(self.f)
        writer = csv.writer(self.f)

        try:
            headers = reader.next()
        except StopIteration:  # handle empty file
            print "Writing headers to csv."
            writer.writerow(fields)
            return None
        else:
            if headers != self.fields:
                if len(set(self.fields) - set(headers)):
                    print >> sys.stderr, "Missing fields in csv header: %s" \
                                         % list(set(self.fields) - set(headers))
                if len(set(headers) - set(fields)):
                    print >> sys.stderr, "Excluded fields in csv header: %s" \
                                         % list(set(headers) - set(self.fields))
                if raw_input("Enter 'q' to abort.\n") == 'q':
                    exit(1)
        finally:
            oldest = None
            #TODO: replace; pretty expensive for large files
            #TODO: fix; does not work seemingly
            for row in reader:
                try:
                    t = ' '.join(row[0:2])
                    t = datetime.datetime.strptime(t, "%m/%d/%y %H:%M")
                except:
                    # Unsuccessful attempt to create datetime.datetime from the row
                    # (could be an empty line, bogus data, etc.); skip to next row
                    continue
                else:
                    oldest = t
            return oldest

    def write_data(self, data):
        try:
            writer = csv.DictWriter(self.f, self.fields)
            for e in data:
                writer.writerow(e)

        except IOError as err:
            print >> sys.stderr, "Issue opening file: %s", self.filename
            print >> sys.stderr, err
            exit(1)

    def __enter__(self):
        return self

    def __exit__(self):
        if self.f:
            self.f.close()
