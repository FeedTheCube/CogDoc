import src
import src.Classes
import src.Classes.DatItem as DI
import src.Classes.DetFilter as DF
import src.Classes.Query as Q


class Util(object):
    #Used for static methods/functions

    def getQueries(xmlSpec, namespace):
        print("retreiving queries")
        queries=[]
        queriesIter = xmlSpec.iter(namespace + "query")
        for query in queriesIter:
            if query[0][0].tag == namespace+"queryRef":
                source = query[0][0].get("refQuery")
            if query[0][0].tag == namespace+"model":
                source = "model"
            qry = Q.Query(
                    _name = query.get("name"),
                    _source = source,
                    _joins = None,
                    _dataItems = Util.getDataItems(query, namespace),
                    #getDataItems,
                    _filters = Util.getDetailFilters(query, namespace),
                    _slicers = None,
                    _element = query
                )
            queries.append(qry)
        return queries
        

    def getDataItems(element, namespace):
        dataItems = []
        dItemsIter = element.iter(namespace+"dataItem")
        for dataItem in dItemsIter:
            dI = DI.DatItem(
                _name = dataItem.get("name"),
                _aggregate = dataItem.get("aggregate"),
                _rollupAggregate = dataItem.get("rollupAggregate"),
                _sort = dataItem.get("sort"),
                _expression = dataItem[0].text,
                _element = dataItem
                )
            dataItems.append(dI)
         
        return dataItems
    

    def getDetailFilters(element, namespace):
        detailedFilters = []
        detFiltIter = element.iter(namespace + "detailFilter")
        if detFiltIter:
            for detFilter in detFiltIter:
                if detFilter.get("usage"):
                    usage = detFilter.get("usage")
                else:
                    usage = "required"
                df = DF.DetFilter(
                    _expression = detFilter[0].text,
                    _usage = usage,
                    _element = detFilter
                    )
                detailedFilters.append(df)
        return detailedFilters