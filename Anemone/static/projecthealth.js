// This script will show the health of the project as circle diagram
// depends on d3
function createHealthchart(urlPath)
{
    var width = 200;
    var height = 200;
    var donutWidth = 45;
    var legendRectSize = 18;
    var legendSpacing = 4;
    var radius = Math.min(width, height) / 2;
    var svg = d3.select('graph')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', 'translate(' + (width / 2) +  ',' + (height / 2) + ')');

    var arc = d3.svg.arc()
        .innerRadius(radius - donutWidth)
        .outerRadius(radius);

    var pie = d3.layout.pie()
        .value(function(d) { return d.count; })
        .sort(null);

    d3.csv(urlPath, function(error, dataset)
    {
        // dataset.forEach(function(d) {
        //     d.count = +d.count;
        // });

        var path = svg.selectAll('path')
            .data(pie(dataset))
            .enter()
            .append('path')
            .attr('d', arc)
            .attr('fill', function(d, i) {
                return dataset[i].color;
            });

        var legend = svg.selectAll('.legend')
            .data(dataset)
            .enter()
            .append('g')
            .attr('class', 'legend')
            .attr('transform', function(d, i) {
                var height = legendRectSize + legendSpacing;
                var offset =  height * dataset.length / 2;
                var horz = -2 * legendRectSize;
                var vert = i * height - offset;
                return 'translate(' + horz + ',' + vert + ')';
            });

        legend.append('rect')
            .attr('width', legendRectSize)
            .attr('height', legendRectSize)
            .style('fill', function(d) { return d.color; })
            .style('stroke',  function(d) { return d.color; });

        legend.append('text')
            .attr('x', legendRectSize + legendSpacing)
            .attr('y', legendRectSize - legendSpacing)
            .text(function(d) { return d.category; });
    });
}
