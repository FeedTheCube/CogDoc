class DetailFilter(object):
    """description of class"""
    def __init__(self, _expression, _usage, _element):
        self.expression = _expression
        self.usage = _usage
        self.element = _element

    def getDetailFilters(element, namespace):
        detailedFilters = []
        detFiltIter = element.iter(namespace + "detailFilter")
        if detFiltIter:
            for detFilter in detFiltIter:
                if detFilter.get("usage"):
                    usage = detFilter.get("usage")
                else:
                    usage = "required"
                df = DetailFilter(
                    _expression = detFilter[0].text,
                    _usage = usage,
                    _element = detFilter
                    )
                detailedFilters.append(df)
        return detailedFilters

