function drawLine(ctx, startX, startY, endX, endY){
    ctx.beginPath();
    ctx.moveTo(startX, startY);
    ctx.lineTo(endX, endY);
    ctx.stroke();
};

function drawArc(ctx, centerX, centerY, radius, startAngle, endAngle){
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.stroke();
};

function drawPieSlice(ctx, centerX, centerY, radius, startAngle, endAngle, color){
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(centerX, centerY);
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.closePath();
    ctx.fill();
};

class Piechart {
    constructor(options) {
        this.options = options;
        this.canvas = options.canvas;
        this.canvas.width = 300;
        this.canvas.height = 300;
        this.ctx = this.canvas.getContext("2d");
        this.ctx.shadowOffsetX = 1;
        this.ctx.shadowOffsetY = 1;
        this.ctx.shadowColor = '#393945';
        this.ctx.shadowBlur = 20;
        this.colors = options.colors;
        this.draw = function () {
            var total_value = 0;
            var color_index = 0;
            for (var categ in this.options.data) {
                var val = this.options.data[categ];
                total_value += val;
            }
            var start_angle = 0;
            for (categ in this.options.data) {
                val = this.options.data[categ];
                var slice_angle = 2 * Math.PI * val / total_value;
                drawPieSlice(
                    this.ctx,
                    this.canvas.width / 2,
                    this.canvas.height / 2,
                    Math.min(this.canvas.width / 2, this.canvas.height / 2),
                    start_angle,
                    start_angle + slice_angle,
                    this.colors[color_index % this.colors.length]
                );
                start_angle += slice_angle;
                color_index++;
            };
            if (this.options.doughnutHoleSize) {
                drawPieSlice(
                    this.ctx,
                    this.canvas.width / 2,
                    this.canvas.height / 2,
                    this.options.doughnutHoleSize * Math.min(this.canvas.width / 2, this.canvas.height / 2),
                    0,
                    2 * Math.PI,
                    "#202029"
                );
            };
        };
    };
};

function chart(canvas, data=sampleData, doughnut=0, legend){
    var Chart = new Piechart(
        {
            canvas:document.getElementById(canvas),
            data:data,
            colors:["#009933", "#fde23e","#f16e23","#57d9ff","#937e88"],
            doughnutHoleSize:doughnut,
            legend:document.getElementById(legend)
        }
    );
    Chart.draw();
};
