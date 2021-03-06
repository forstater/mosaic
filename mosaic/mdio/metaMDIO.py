"""
	Interface class to write and query metadata 

	:Created:	3/1/2014
 	:Author: 	Arvind Balijepalli <arvind.balijepalli@nist.gov>
	:License:	See LICENSE.TXT
	:ChangeLog:
	.. line-block::
		11/9/14 	AB 	Added an interface to read/write the output log of an analysis from/to a DB.
		3/1/14		AB	Initial version
"""
import os
import mosaic.utilities.mosaicTiming as mosaicTiming
from abc import ABCMeta, abstractmethod
from mosaic.utilities.mosaicLogFormat import mosaic_property

__all__ = ["metaMDIO", "InsufficientArgumentsError"]

class InsufficientArgumentsError(Exception):
	pass

class metaMDIO(object):
	"""
		.. warning:: |metaclass|

		This class provides the skeleton for storing metadata
		generated by algorithms. It also provides an interface to query metadata, for example in a 
		SQL database.

		:Properties:
			- `dbColumnNames` : a list of database column names
	"""
	__metaclass__=ABCMeta

	def __init__(self):
		self.pid=os.getpid()
		
		# Setup function timing
		self.timingObj=mosaicTiming.mosaicTiming()

	def initDB(self, **kwargs):
		"""
			Initialize a new database file.

			:Parameters: 
			The arguments passed to init change based on the method of file IO selected, in addition to 
			the common args below:
				- `dbPath` :		directory to store the MD database ('<full path to data directory>')
				- `colNames` : 	list of text names for the columns in the tables
				- `colNames_t` :	list of data types for each column. 
		"""
		# start by setting all passed keyword arguments as class attributes
		for (k,v) in kwargs.iteritems():
			setattr(self, k, v)

		if not hasattr(self, 'dbPath'):
			raise InsufficientArgumentsError("Missing arguments: 'dbPath' must be supplied to initialize {0}".format(type(self).__name__))
		if not hasattr(self, 'colNames'):
			raise InsufficientArgumentsError("Missing arguments: 'colNames' must be supplied to initialize {0}".format(type(self).__name__))
		if not hasattr(self, 'colNames_t'):
			raise InsufficientArgumentsError("Missing arguments: 'colNames_t' must be supplied to initialize {0}".format(type(self).__name__))

		self._initdb(**kwargs)

	def openDB(self, dbname, **kwargs):
		"""
			Open an existing database file.

			:Parameters: 
				- `dbname` :		directory to store the MD database ('<full path to data directory>')

			.. seealso:: The arguments passed to init change based on the method of file IO selected, in addition to the common args.
		"""
		self._opendb(dbname, **kwargs)

	@abstractmethod
	def _dbfile(self):
		"""
			.. important:: |abstractmethod|

			Return the full path and filename to the database.
		"""
		pass

	@abstractmethod
	def _opendb(self, dbname, **kwargs):
		"""
			.. important:: |abstractmethod|
		"""
		pass

	@abstractmethod
	def _initdb(self, **kwargs):
		"""
			.. important:: |abstractmethod|
		"""
		pass

	@abstractmethod
	def closeDB(self):
		"""
			.. important:: |abstractmethod|
		"""
		pass

	@abstractmethod
	def writeRecord(self, data, table=None):
		"""
			.. important:: |abstractmethod|

			Write data to a specified table. By default table 
			is None. In this case sub-classes should fall back 
			to writing data to a default table.
		"""
		pass

	@abstractmethod
	def writeSettings(self, settingsstring):
		"""
			.. important:: |abstractmethod|

			Write the settings JSON object to the database.

			:Args:
				- `settingsstring` : a JSON_ formatted settings string.
		"""
		pass

	@abstractmethod
	def writeAnalysisLog(self, analysislog):
		"""
			.. important:: |abstractmethod|

			Write the analysis log string to the database. Note that subsequent calls to this method will overwrite the analysis log entry.

			:Args:
				- `analysislog` :	analysis log string to save
		"""
		pass

	@abstractmethod
	def writeAnalysisInfo(self, infolist):
		"""
			.. important:: |abstractmethod|

			Write analysis information to the database. Note that subsequent calls to this method will overwrite the analysis inoformation entry in the table.

			:Args:
				- `infolist` : A list of strings in the following order	[ datPath, dataType, partitionAlgorithm, processingAlgorithm, filteringAlgorithm].
								`datPath` 				: full path to the data directory

								`dataType`				: type of data processed (e.g. ABF, QDF, etc.)
								
								`partitionAlgorithm`	: name of partition algorithm (e.g. eventSegment)
								
								`processingAlgorithm`	: name of event processing algorithm (e.g. multStateAnalysis)
								
								`filteringAlgorithm`	: name of filtering algorithm (e.g. waveletDenoiseFilter) or None if no filtering was performed.
		"""
		pass

	@abstractmethod
	def readSettings(self):
		"""
			.. important:: |abstractmethod|

			Read JSON settings from the database.
		"""
		pass

	@abstractmethod
	def readAnalysisLog(self):
		"""
			.. important:: |abstractmethod|

			Read the analysis log from the database.
		"""
		pass

	@abstractmethod
	def readAnalysisInfo(self):
		"""
			.. important:: |abstractmethod|

			Read analysis information from the database.
		"""
		pass

	@abstractmethod
	def _colnames(self, table=None):
		"""
			.. important:: |abstractmethod|
		"""
		pass

	@abstractmethod
	def _coltypes(self, table=None):
		"""
			.. important:: |abstractmethod|
		"""
		pass

	@abstractmethod
	def queryDB(self, query):
		"""
			.. important:: |abstractmethod|

			Query a database. 
			:Parameters:
				- `query` : query string 

			.. seealso:: See specific implementations of metaMDIO for query syntax.
		"""
		pass

	@mosaic_property 
	def mdColumnNames(self):
		return self._colnames()

	@mosaic_property 
	def mdColumnTypes(self):
		return self._coltypes()

	@mosaic_property 
	def dbFile(self):
		return self._dbfile()
		
	def _generateRecordKey(self):
		return float(self.timingObj.time()+self.pid)


