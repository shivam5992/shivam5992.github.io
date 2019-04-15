aerographApp.controller('RootController', function($rootScope,$http) {
    
	$rootScope.input={
		selectedGraph:'combo' ,
		legendSelection:"Country"
	} ;
	
	$rootScope.initGraph=function() {
		$rootScope.width=document.getElementById("d3js-column").clientWidth-30;
		$rootScope.height=700;
		
		$rootScope.force = d3.layout.force()
		    .size([$rootScope.width,$rootScope.height]);
		
		$rootScope.svg = d3.select("#d3js-fdgraph").append("svg")
		    .attr("width", $rootScope.width)
		    .attr("height", $rootScope.height);
		
		$rootScope.countryColors = d3.scale.linear().domain([0 , 0.15 , 0.20 , 0.25 , 0.30, 0.35,0.40,0.42,0.45,0.50,1])
			.range(["#7f7f7f", "#e377c2", "#8c564b", "#9467bd" , "#d62728" , "#2ca02c" , "grey" , "orange","#637939","#e7ba52","blue"]);
		$rootScope.ageColors = d3.scale.linear().domain([0, 20, 30, 40, 50 , 60, 120]).range(["#7f7f7f", "#e377c2", "#8c564b", "#9467bd" , "#d62728" , "#2ca02c" , "#1f77b4" ]);
		$rootScope.genderColors = d3.scale.linear().domain([0,0.5,1]).range(["red", "grey", "blue"]);
		$rootScope.naColors = d3.scale.linear().domain([0,1]).range(["#31a354","#c6dbef"]);
	}
	
	$rootScope.loadGraph=function() {
		var file=$rootScope.input.selectedGraph+".json" ;
		$http.get(file).then(function(res){
			$rootScope.graph=res.data ;
			$rootScope.params=$rootScope.graph.params ;
			$rootScope.params.detailLevel=4 ;  
			$rootScope.flattenGraph() ;
	        $rootScope.updateGraph() ;
	        $rootScope.updateLegendHtml() ;
	        $rootScope.makeKnnChart() ;
	    });
	}
	
	$rootScope.updateGraph=function() {
		$rootScope.force
		    .stop()
		    .linkStrength(function(d){return d.similarity})
		    .linkDistance($rootScope.linkDistance)
		    .charge(- $rootScope.params.charge)
		    .gravity($rootScope.params.gravity)
  	      	.nodes($rootScope.flattened.nodes)
		    .links($rootScope.flattened.links)
		    .start();
		
		$rootScope.svg.selectAll("*").remove();
		
		var link = $rootScope.svg.selectAll(".link")
	      .data($rootScope.flattened.links)
	      .enter().append("line")
	      .attr("class", "link")
	      .style("stroke-width", function(d) { return 1; });
	
		var node = $rootScope.svg.selectAll(".node")
	      .data($rootScope.flattened.nodes)
	      .enter().append("circle")
	      .attr("class", "node")
	      .attr("r", function(d) { return Math.round(1+2*Math.log(1+d.size)); })
	      .style("fill", $rootScope.legendColors)
	      .call($rootScope.force.drag);
	
		node.append("title").text(function(d) {  return 'UID_'+d.size; });
		
		$rootScope.force.on("tick", function() {
		    link.attr("x1", function(d) { return d.source.x; })
		        .attr("y1", function(d) { return d.source.y; })
		        .attr("x2", function(d) { return d.target.x; })
		        .attr("y2", function(d) { return d.target.y; });
		
		    node.attr("cx", function(d) { return d.x; })
		        .attr("cy", function(d) { return d.y; });
		  });
		
	}
	
	$rootScope.flattenGraph=function() {
		var upToLevel=$rootScope.params.detailLevel ;
		var ans={} ;
		ans.nodes=[] ;
		ans.links=[] ;
		var dictionary=new Array() ;
		$rootScope.addNodesAndLinks($rootScope.graph.root,ans.nodes,ans.links,dictionary,0,upToLevel) ;
		$rootScope.fixLinks(ans.links,dictionary) ;
		$rootScope.flattened=ans ;
	}

	$rootScope.addNodesAndLinks=function(element,nodes,links,dictionary,currentIndex,upToLevel) {
		if (element.level==0) {
			element.x=0 ;
			element.y=0 ;
		}
		nodes.push(element) ;
		dictionary[element.id]=currentIndex ;
		currentIndex++ ;
		for (var i=0 ; element.children!=null && i<element.children.length ; i++) {
			var child=element.children[i] ;
			nodes.push(child) ;
			dictionary[child.id]=currentIndex ;
			currentIndex++ ;
			var parentToChild={sourceId:element.id,targetId:child.id,similarity:1.0,level:element.level} ;
			links.push(parentToChild) ;
		}
		for (var i=0 ; element.links!=null && i<element.links.length ; i++) {
			var originalLink=element.links[i]
			var newLink={sourceId:originalLink.sourceId,targetId:originalLink.targetId,similarity:originalLink.similarity} ;
			newLink.level=element.level ;
			links.push(newLink) ;
		}
		if (element.level<(upToLevel-1)) {
			for (var i=0 ; element.children!=null && i<element.children.length ; i++) {
				currentIndex=$rootScope.addNodesAndLinks(element.children[i],nodes,links,dictionary,currentIndex,upToLevel) ;
			}
		}
		return currentIndex ;
	}

	$rootScope.fixLinks=function(links,dictionary) {
		for (var i=0 ; links!=null && i<links.length ; i++) {
			var link=links[i] ;
			link.source=dictionary[link.sourceId] ;
			link.target=dictionary[link.targetId] ;
		}
	}

	$rootScope.linkDistance=function(link) {
		if (link.level==0) {
			return $rootScope.params.linkDistance0 ;
		} else if (link.level==1) {
			return $rootScope.params.linkDistance1 ;
		} else if (link.level==2) {
			return $rootScope.params.linkDistance2 ;
		} else if (link.level==3) {
			return $rootScope.params.linkDistance3 ;
		} else if (link.level==4) {
			return $rootScope.params.linkDistance4 ;
		} else {
			return 0 ;
		}
	}
	
	$rootScope.setLegendSelection=function() {
		if ($rootScope.svg==null) {
			return ;
		} else {
			$rootScope.svg.selectAll(".node").style("fill", $rootScope.legendColors) ;
			$rootScope.updateLegendHtml() ;
		}
	}

	$rootScope.legendColors=function(d) { 
		var legendSelection=$rootScope.input.legendSelection ;
		if (legendSelection=="Country") {
			return $rootScope.countryColors(d.ndf) ; 	
		} else if (legendSelection=="Age") {
			return $rootScope.ageColors(d.age) ; 	
		} else if (legendSelection=="Gender") {
			return $rootScope.genderColors(d.male) ;
		} else if (legendSelection=="NAs") {
			return $rootScope.naColors(d.na) ;
		}		
	}

	$rootScope.updateLegendHtml=function() {
		var legendSelection=$rootScope.input.legendSelection ;
		var labels=null ;
		var values=null ;
		var colors=null ;
		if (legendSelection=="Country") {
			labels=["US", "France" , "Italy" , "Spain", "UK","Austria","Canada","Netherland","Germany","Portugal", "NotBooked"]
			values=[0 , 0.15 , 0.20 , 0.25 , 0.30, 0.35,0.40,0.42,0.45,0.50,1] ;
			colors=$rootScope.countryColors ;
		} else if (legendSelection=="Age") {
			labels=[0,10,20,30,40,50,60,80,100,120] ;
			values=[0,10,20,30,40,50,60,80,100,120] ;
			colors=$rootScope.ageColors ;
		} else if (legendSelection=="Gender") {
			labels=["100% FEMALE", "75% FEMALE" , "50% / 50%", "75% MALE" , "MALE"] ;
			values=[0 , 0.25 , 0.5 , 0.75 , 1] ;
			colors=$rootScope.genderColors ;
		} else if (legendSelection=="NAs") {
			labels=["0%", "25%" , "50%" , "75%" , "100%"] ;
			values=[0 , 0.25 , 0.5 , 0.75 , 1] ;
			colors=$rootScope.naColors ;
		}
		html="<table class='table table-condensed'>\n" ;
		for (var i=0 ; i<values.length ; i++) {
			html+="<tr><td><div style='width:15px;height:15px;border-style:solid;border-width:thin;border-color:gray;background-color:"+colors(values[i])+"'></div></td><td>"+labels[i]+"</td></tr>\n" ;
		}
		html+="</table>" ;
		$("#legendTable").html(html) ;
	}
	
	$rootScope.updateCharge=function() {
		var charge=-$rootScope.params.charge ;
		$rootScope.force
			.stop() 
			.charge(charge)
			.start() ;
	}
	
	$rootScope.updateGravity=function() {
		var gravity=$rootScope.params.gravity ;
		$rootScope.force
			.stop() 
			.gravity(gravity) 
			.start() ;
	}
	
	$rootScope.updateLinkDistance=function() {
		var gravity=$rootScope.params.gravity ;
		$rootScope.force
			.stop() 
			.linkDistance($rootScope.linkDistance)
			.start() ;
	}
	
	$rootScope.updateDetailLevel=function() {
		$rootScope.flattenGraph() ;
		$rootScope.updateGraph() ;
	}
	
	$rootScope.makeKnnChart=function() {
		var scores=$rootScope.graph.scores ;
		var data=[] ;
		for (var i=0 ; i<scores.length ; i++) {
			data.push([(i+1),scores[i]]) ;
		}
		$('#knn-chart').highcharts({
            title: {
                text: ''
            },
            yAxis: {
                title: {text: 'Score'}
            },
            legend: {
                enabled: false
            },
            chart: {
                zoomType: 'x'
            },
            plotOptions: {
                area: {
                    fillColor: {
                        linearGradient: {
                            x1: 0,
                            y1: 0,
                            x2: 0,
                            y2: 1
                        },
                        stops: [
                            [0, Highcharts.getOptions().colors[0]],
                            [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                        ]
                    },
                    marker: {
                        radius: 2
                    },
                    lineWidth: 1,
                    states: {
                        hover: {
                            lineWidth: 1
                        }
                    },
                    threshold: null
                }
            },
            series: [{
                type: 'area',
                name: 'Score',
                data: data
            }]
        });
	}
	
	$rootScope.initGraph() ;
	$rootScope.loadGraph() ;
	
});