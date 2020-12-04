
const data = [...Array(100).keys()].map(ele => {return {head:String(Math.floor(ele/10)), tail:String(ele%10), value:0}})

const tsData = [...Array(1000).keys()].map(ele => {return {x: Math.floor(ele/10), y: (ele % 10), value: 0 }});


while (num.length > 0) {
    var lastNumArr = num.pop().split(',').sort().map(ele => ele.substr(1))
    for (var i = 0; i < 5; i++){
        var idx = parseFloat(lastNumArr[i]+lastNumArr[i+1])
        data[idx].value += 1
    }

   tsData[parseFloat(lastNumArr[2]+lastNumArr[3]+lastNumArr[4])].value += 1
}

const axisRange = [...Array(10).keys()];

const createContainer = function(widgetName, target){
	var description = "div[widgetname='" + widgetName + "']";
	var container = $(description);
	var width = +container.width();
	var height = +container.height();
	container.empty();
	container.append("<svg width=" + width+ " height="+ height +" class='hist_"+target+"' id='"+target+"' style='background:#fff;'></svg>")
}

const render = (dta, svgObject) =>{
    const margin = { top:50, right:30, bottom: 30, left: 30};
    const width = +svgObject.attr('width');
    const height = +svgObject.attr('height');
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;;
    const gridSize = Math.floor(innerHeight/11);
    const dim_1 = axisRange;
    const dim_2 = axisRange;
    const maxValue = d3.max(dta, d => d.value) || 1
    const minValue = d3.min(dta.filter(ele => ele.value > 0), d => d.value) || 0
    const colorScale = d3.scaleSequential().domain([minValue, maxValue])
    .interpolator(d3.interpolateYlOrRd);
    
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d){
            return "台號: "+d.head+d.tail + "<br>開出次數: " +d.value;
        })

    svgObject.call(tip);

    const g = svgObject.append('g')
        .attr('transform', 'translate('+(width-innerWidth)+','+(margin.top+30)+")");
    
    const yAxisG = svgObject.append('g')
        .attr('transform', 'translate('+(width-innerWidth+margin.left/2)+", "+(margin.top+30)+")")

    const dim1Labels = yAxisG.selectAll('.dim1Label')
        .data(dim_1)
        .enter().append('text')
        .text(d => d)
        .attr('x', 0)
        .attr('y', function(d, i){ return i * gridSize })
        .attr("transform", "translate(0," + (-gridSize/3)  + ")")
        .style('text-anchor', "middle")
        .style('font-family', '微軟正黑體')
        .style('font-weight', 'bold')
        .style('fill', 'black');
    
    const yTitle = yAxisG.append('text')
        .attr('transform', 'translate('+(-margin.left)+", "+(4*gridSize)+")");

    yTitle.selectAll('word')
        .data(["尾","號"])
        .enter().append('tspan')
        .attr('x', 0)
        .attr('y', 0)
        .attr('dy', function(d, i){return i*1.5+"em"})
        .text(d => d)
        .style('font-family', '微軟正黑體')
        .style('fill', 'black')
        .style('font-weight', 'bold')

    const xAxisG = svgObject.append('g')
        .attr('transform', 'translate('+(width-innerWidth+margin.left/2)+', '+(margin.top+30+gridSize*9.5)+")")

    const dim2Labels = xAxisG.selectAll('.dim2Label')
        .data(dim_2)
        .enter().append('text')
        .text(d => d)
        .attr('x', function(d, i){ return i * gridSize +margin.left})
        .attr('y', 0)
        .style('text-anchor', 'middle')
        .style('font-family', '微軟正黑體')
        .style('font-weight', 'bold')
        .style('fill', 'black')
    
    xAxisG.append('text')
        .attr('x', gridSize*5)
        .attr('y', margin.bottom*2/3)
        .text('頭號')
        .style('font-family', '微軟正黑體')
        .style('font-weight', 'bold')
        .style('fill', 'black')

    const heatmap = g.selectAll('dim2')
        .data(dta)
        .enter().append('rect')
        .attr('x', d => {return (d.head - 1) * gridSize + gridSize+margin.left; })
        .attr('y', d => {return (d.tail - 1) * gridSize; })
        .attr('rx', 4)
        .attr('ry', 4)
        .attr('class', 'dim2 bordered')
        .attr('width', gridSize - 2)
        .attr('height', gridSize - 2)
        .attr('class', 'square')
        .style('fill', d => {if( d.value === 0){return "#adacac"} else {return colorScale(d.value)}})
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    // add color scale legend
    var linear = d3.scaleLinear()
        .domain([maxValue,minValue])
        .range([colorScale(maxValue), colorScale(minValue)]);

    g.append("g")
        .attr("class", "legendLinear")
        .attr("transform", "translate("+(gridSize*10+margin.left*2)+","+(margin.top)+")")
        .style('font-family', '微軟正黑體')
        .style('font-size', "10px")
        .style('font-weight', 'bold');

    var legendLinear = d3.legendColor()
        .shapeWidth(30)
        .cells(10)
        .scale(linear)
        .title("開出次數參照");


    svgObject.select(".legendLinear")
        .call(legendLinear);

    d3.select(".legendLinear").selectAll('text')
    		.style('fill', 'black');

    d3.select('.legendTitle').attr('font-size', '14px');


    svgObject.append('text')
        .attr('class', 'title')
        .attr('y', 20)
        .attr('x', 20)
        .attr('transform', 'translate(20, 10)')
        .text('台號   開獎熱區')
        .style('font-family', '微軟正黑體')
        .style('font-weight', 'bold')
        .style('font-size', '19px')
        .style('fill', 'black');
        
}

const bubbleRender = (dta, svgObject) => {
    const xValue = d => d.x;
    const yValue = d => d.y;
    
    const margin = { top: 60, right: 40, bottom: 80, left: 60};
    const width = parseFloat(svgObject.attr('width'))
    const innerWidth = width - margin.left - margin.right;
    const height = parseFloat(svgObject.attr('height'))
    const innerHeight = height - margin.top - margin.bottom;
    const maxValue = d3.max(dta, ele => ele.value) || 1
    const minValue = d3.min(dta.filter(ele => ele.value > 0), d => d.value) || 0
    const circleRadius = 10
    const radiusTimes = d => {return (d.value-minValue+1)/(maxValue-minValue+1)*circleRadius}


    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d){
            return "特三: "+d.x+d.y + "<br>開出次數: " +d.value;
        })

    svgObject.call(tip);
        

    const xScale = d3
        .scaleLinear()
        .domain(d3.extent(dta, xValue))
        .range([0, innerWidth])
        .nice();
    
    const yScale = d3
        .scaleLinear()
        .domain(d3.extent(dta, yValue))
        .range([innerHeight, 0])
        .nice()

    const g = svgObject
        .append('g')
        .attr('transform', 'translate('+margin.left+', '+margin.top+')')

    const xAxis = d3
        .axisBottom(xScale)
        .tickSize(-innerHeight)
        .tickPadding(15);

    const yAxis = d3
        .axisLeft(yScale)
        .tickSize(-innerWidth)
        .tickPadding(10);

    const yAxisG = g.append('g').call(yAxis);
    yAxisG.selectAll('.domain').remove();

    
    const yLabel = yAxisG
    .append("text")
    .attr("class", "axis-label")
    //.attr("y", innerHeight/2+margin.top)
    //.attr("x", -margin.left/2)
    .attr("fill", "black")
    .attr("text-anchor", "middle")
    
    yLabel.selectAll('word')
        .data(["特","三", "末", "碼"])
        .enter().append('tspan')
        .attr('x', -margin.left/2)
        .attr('y', innerHeight/2)
        .attr('dy', (d, i) => {return i*1.1 + "em"})
        .text(d => d)
        .style('font-family', '微軟正黑體')
        .style('font-size', '0.9rem')
        .style('font-weight', 'bold')
        .style('fill', 'black');


  const xAxisG = g
    .append("g")
    .call(xAxis)
    .attr("transform", "translate(0,"+ innerHeight+")");

  xAxisG.select(".domain").remove();

  xAxisG
    .append("text")
    .attr("class", "axis-label")
    .attr("y", margin.bottom*0.75)
    .attr("x", innerWidth / 2)
    .text("特三前二碼")
    .style('font-family', '微軟正黑體')
    .style('font-size', '0.9rem')
    .style('font-weight', 'bold')
    .style("fill", "black");

  g.selectAll('circle')
    .data(dta.filter(ele => ele.value != 0))
    .enter()
    .append('circle')
    .attr('cy', d => yScale(yValue(d)))
    .attr('cx', d => xScale(xValue(d)))
    .attr('r', d => radiusTimes(d))
    .attr('fill', "#007C59")
    .attr('fill-opacity', d => {return radiusTimes(d)/circleRadius})
    .on('mouseenter', tip.show)
    .on('mouseleave', tip.hide)

  svgObject.append('text')
    .attr('x', margin.left)
    .attr('y', margin.top/2)
    .text('特三  開獎次數氣泡圖')
    .style('font-weight', 'bold')
    .style('fill', 'black')
    .style('font-family', '微軟正黑體')
    .style('font-size', '1.25rem');

   yAxisG.selectAll('text')
   	.style('fill', 'black');


   xAxisG.selectAll('text')
   	.style('fill', 'black');


}

setTimeout(function (){ 
createContainer('LABEL0', 'TH');
createContainer('LABEL1', 'TS');

const svgTH = d3.select('#TH');
const svgTS = d3.select('#TS');

render(data, svgTH)
bubbleRender(tsData, svgTS)

} ,300);