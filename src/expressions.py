from sortedcontainers import SortedDict


class expression:
    isinstances: dict[str, 'expression'] = {}
    def __init__(self, operator: str = None, 
                 singleRowValidater: function[str, str, bool] = None,
                 partialIndexFunction: function[dict, str, list[id]] = None, 
                 indexRangeFunction: function = None
                 ):

                 self.operator = operator
                 self.singleRowValidater = singleRowValidater
                 self.partialIndexFunction = partialIndexFunction
                 self.indexRangeFunction = indexRangeFunction

                 
                 expression.isinstances[operator] = self
    
    
    
    
    
def initialVanilaIndexFunction(data: dict, field: str, ids: list[int]) -> list[int]:
        return data.get(field, {}).get(ids, [])


def initialGreaterThanRangeIndex(data: dict, field: str, startRange: any) -> list[int]:
    collumnIndex =  data.get(field, {})
    nestedResults = collumnIndex.irange(startRange)
    rowIds = []
    for rowIdList in nestedResults:
        rowIds.extend(rowIdList)
    return rowIds



def initialLessThanRangeIndex(data: dict, field: str, startRange: any) -> list[int]:
    collumnIndex =  data.get(field, {})
    collumnIndex: SortedDict
    nestedResults = collumnIndex.irange(type(startRange)() , startRange)
    rowIds = []
    for rowIdList in nestedResults:
        rowIds.extend(rowIdList)
    return rowIds



def initialMapRangeFunction(data: dict, field: str, startRange: any, endRange: any) -> list[int]:
    """
    startRange: any, endRange: any -- works for any map type (map<any>)
    """
    return data.get(field, {}).irange(startRange, endRange)

    
    
expression("==", singleRowValidater=lambda a, b: a == b,
            partialIndexFunction=initialVanilaIndexFunction)


expression(">=", singleRowValidater=lambda x, y: int(x) >= int(y),
            partialIndexFunction=initialVanilaIndexFunction,
            initialIndexRangeFunction=initialMapRangeFunction)