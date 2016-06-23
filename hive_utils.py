def generate_hive_table(file_to_load, delimiter, hdfs_dir, tab_name, line_terminator='\n'):
    """
    Generated a hive table based on the column header of a delimited flat file
    :param file_to_load: local path of flat file with column header definition
    :param delimiter: record separator of file (usually something like pipe '|' or comma ','
    :param hdfs_dir: directory on hdfs where file is located (hive will point to this directory)
    :param tab_name: name of table in hive
    :param line_terminator: character(s) which indicate the end of a line in the flat file (defaults to \n)
    :return: hive query string
    """

    # TODO: Add functionality to point to existing file in HDFS and build table definition from there
    # TODO: Add functionality to connect to hive client and create table automatically
    # TODO: More options than just external table and directory location

    if line_terminator == '\n':
        line_terminator = '\\n'

    with open(file_to_load) as f:
        first_line = f.readline()

    columns = first_line.split('|')

    query = 'CREATE EXTERNAL TABLE ' + tab_name + '(\n'

    for c in columns:
        query += c.replace('\n', '') + ' STRING,\n'

    # trim line feed and final comma
    query = query[:-2]

    query += '\n)'

    query += "\nROW FORMAT"
    query += "\nDELIMITED FIELDS TERMINATED BY '" + delimiter + "'"
    query += "\nLINES TERMINATED BY '" + line_terminator + "'"
    query += "\nSTORED AS TEXTFILE"
    query += "\nLOCATION '" + hdfs_dir + "'"
    query += '\nTBLPROPERTIES ("skip.header.line.count"="1")'
    query += ";"

    return query
