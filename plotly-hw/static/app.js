function Charts(sampleId) {d3.json("data/samples.json").then(BBD => {
        console.log(BBD)
        //collecting important data points from the metadata
        var data = BBD.samples;
        var array = data.filter(s => s.id == sampleId);
        var sample = array[0];
        var iD = sample.otu_ids;
        var  = sample.otu_labels;
        var values = sample.sample_values;
        
        //Horizontal Bar Graph
        var trace1 = [{
            type: "bar",
            orientation: "h",
            x: values.slice(0, 10).reverse(),
            y: iD.slice(0, 10).map(id => id).reverse(),
            text: otuLabel.slice(0, 10).reverse(),
        }];

        var layout1 = {
            title: "Top 10 OTUs by Sample",
            xaxis: {title: "# of OTUs Present"},
            autosize: true,
        };

        Plotly.newPlot("bar", trace1, layout1);

        //Bubble Graph at the bottom
        var trace2 = [{
            type: "scatter",
            mode: "markers",
            x: iD,
            y: values,
            text: otuLabel,
            marker: {
                size: values,
                color: iD,
                colorscale: "earth"
            }
        }];

        var layout2 = {
            title: "Number of Microbes Present by Sample",
            yaxis: {title: "# of OTUs"},
            xaxis: {title: "OTU ID#"},
        };

        Plotly.newPlot("bubble", trace2, layout2);

    });
}

//function for metadata
function metaData(sampleId) {
    d3.json("data/samples.json").then(BBD => {
        var metadata = BBD.metadata;
        var meta = metadata.filter(m => m.id == sampleId);
        var result = meta[0];
        var section = d3.select("#sample-metadata");
        section.html("");

        Object.entries(result).forEach(([key, value]) => {
            var info = `${key}: ${value}`;
            section.append("p").text(info);
        });
    });
}

//function for optionChanged
function optionChanged(newSampleId) {
    Charts(newSampleId);
    metaData(newSampleId);
}

//init function, starting on first patient option. 
function init() {
    var selector = d3.select("#selDataset");
    d3.json("data/samples.json").then(BBD => {
        var names = BBD.names;
        names.forEach((sampleId) => {
            selector.append("option")
                .text(sampleId)
                .property("value", sampleId);
        });
        var sampleId = names[0];
        Charts(sampleId);
        metaData(sampleId);
    });
}
init();

