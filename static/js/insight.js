am5.ready(function () {

    // -----------------------------
    // HELPERS
    // -----------------------------
    function showView(viewId) {
        const dayView = document.getElementById("day-view");
        const weekView = document.getElementById("week-view");
        const monthView = document.getElementById("month-view");
        const yearView = document.getElementById("year-view");

        let raw = "";

        switch (viewId) {
            case "day-view":
                dayView.style.display = "flex";
                weekView.style.display = "none";
                monthView.style.display = "none";
                yearView.style.display = "none";
                raw = document.getElementById("allData-day").textContent;
                break;

            case "week-view":
                dayView.style.display = "none";
                weekView.style.display = "flex";
                monthView.style.display = "none";
                yearView.style.display = "none";
                raw = document.getElementById("allData-week").textContent;
                break;

            case "month-view":
                dayView.style.display = "none";
                weekView.style.display = "none";
                monthView.style.display = "flex";
                yearView.style.display = "none";
                raw = document.getElementById("allData-month").textContent;
                break;

            case "year-view":
                dayView.style.display = "none";
                weekView.style.display = "none";
                monthView.style.display = "none";
                yearView.style.display = "flex";
                raw = document.getElementById("allData-year").textContent;
                break;

            default:
                console.error("Unknown view selected:", viewId);
                return [];
        }

        if (!raw || !raw.trim()) {
            console.warn("No JSON data found for view:", viewId);
            return [];
        }

        return JSON.parse(raw);
    }

    // -----------------------------
    // TRANSACTION CATEGORIES
    // -----------------------------
    function computeTransactionCategories(allData) {
        const category = {
            "housing": 0, "groceries": 0, "bills": 0, "transport": 0, "entertainment": 0,
            "shopping": 0, "selfcare": 0, "hobbies": 0, "savings": 0, "investments": 0,
            "debt": 0, "travel": 0, "gifts": 0, "medical": 0, "coffee": 0, "takeaway": 0,
            "subscriptions": 0, "beauty": 0, "home": 0, "car": 0
        };

        allData.forEach(day => {
            if (Array.isArray(day.transactions)) {
                day.transactions.forEach(t => {
                    const key = t.category.toLowerCase();
                    if (category.hasOwnProperty(key)) {
                        category[key] += t.amount;
                    }
                });
            }
        });

        console.log("Final category totals:", category);
        return category;
    }

    // -----------------------------
    // EXERCISE CATEGORIES
    // -----------------------------
    function computeExerciseCategories(allData) {
        const exerciseCategory = {
            "running": 0,
            "cycling": 0,
            "swimming": 0,
            "weightlifting": 0,
            "yoga": 0,
            "hiking": 0,
            "other": 0
        };

        allData.forEach(day => {
            if (Array.isArray(day.exercise)) {
                day.exercise.forEach(e => {
                    const key = e.name.toLowerCase().replace(/\s+/g, "");
                    if (exerciseCategory.hasOwnProperty(key)) {
                        exerciseCategory[key] += e.duration; // or calories if you prefer
                    }
                });
            }
        });

        return exerciseCategory;
    }

    // -----------------------------
    // CHART CREATION
    // -----------------------------
    let transactionRoot = null;
    let exerciseRoot = null;

    // -----------------------------
    // TRANSACTION BAR CHART
    // -----------------------------
function buildTransactionChart(viewId, categoryTotals) {
    if (transactionRoot) {
        transactionRoot.dispose();
    }

    const suffix = viewId.replace("-view", "");
    const divId = `transaction-chartdiv-${suffix}`;

    transactionRoot = am5.Root.new(divId);

    transactionRoot.setThemes([
        am5themes_Animated.new(transactionRoot)
    ]);

    // Soft pastel colour palette (correct usage)
    const colors = am5.ColorSet.new(transactionRoot, {
        colors: [
            am5.color("#E194A8"),
            am5.color("#EEB0B5"),
            am5.color("#C9A7EB"),
            am5.color("#A5B4FC"),
            am5.color("#8BD3E6"),
            am5.color("#F7C8E0"),
            am5.color("#F9E2AE")
        ],
        reuse: true
    });

    const chart = transactionRoot.container.children.push(am5xy.XYChart.new(transactionRoot, {
        panX: false,
        panY: false,
        wheelX: "none",
        wheelY: "none",
        paddingLeft: 0,
        paddingRight: 10,
        background: am5.Rectangle.new(transactionRoot, {
            fill: am5.color(0x000000),
            fillOpacity: 0.1,
            cornerRadiusTL: 12,
            cornerRadiusTR: 12
        })
    }));

    const cursor = chart.set("cursor", am5xy.XYCursor.new(transactionRoot, {}));
    cursor.lineY.set("visible", false);

    const xRenderer = am5xy.AxisRendererX.new(transactionRoot, {
        minGridDistance: 20
    });

    xRenderer.labels.template.setAll({
        rotation: -90,
        centerY: am5.p50,
        centerX: am5.p100,
        paddingRight: 10,
        fill: am5.color("#ffffff"),
        fontSize: 12
    });

    const xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(transactionRoot, {
        categoryField: "category",
        renderer: xRenderer
    }));

    const yRenderer = am5xy.AxisRendererY.new(transactionRoot, {
        strokeOpacity: 0
    });

    yRenderer.labels.template.setAll({
        fill: am5.color("#ffffff"),
        fontSize: 12
    });

    const yAxis = chart.yAxes.push(am5xy.ValueAxis.new(transactionRoot, {
        renderer: yRenderer
    }));

    const series = chart.series.push(am5xy.ColumnSeries.new(transactionRoot, {
        name: "Spending",
        xAxis: xAxis,
        yAxis: yAxis,
        valueYField: "value",
        categoryXField: "category",
        tooltip: am5.Tooltip.new(transactionRoot, {
            labelText: "{valueY}",
            background: am5.Rectangle.new(transactionRoot, {
                fill: am5.color("#000000"),
                fillOpacity: 0.6
            })
        })
    }));

    series.columns.template.setAll({
        cornerRadiusTL: 6,
        cornerRadiusTR: 6,
        strokeOpacity: 0,
        shadowColor: am5.color("#000000"),
        shadowBlur: 8,
        shadowOffsetY: 4
    });

    // Correct colour assignment
    series.columns.template.adapters.add("fill", (fill, target) => {
        return colors.getIndex(series.columns.indexOf(target));
    });

    const transactionData = Object.entries(categoryTotals)
        .filter(([_, value]) => value > 0)
        .map(([key, value]) => ({
            category: key,
            value: value
        })).sort((a, b) => b.value - a.value);

    xAxis.data.setAll(transactionData);
    series.data.setAll(transactionData);

    series.appear(1000);
    chart.appear(1000, 100);
}

    // -----------------------------
    // EXERCISE PIE CHART
    // -----------------------------
    function buildExerciseChart(viewId, exerciseTotals) {
    if (exerciseRoot) {
        exerciseRoot.dispose();
    }

    const suffix = viewId.replace("-view", "");
    const divId = `exercise-chartdiv-${suffix}`;

    exerciseRoot = am5.Root.new(divId);

    exerciseRoot.setThemes([
        am5themes_Animated.new(exerciseRoot)
    ]);

    const chart = exerciseRoot.container.children.push(
        am5percent.PieChart.new(exerciseRoot, {
            layout: exerciseRoot.verticalLayout,
            innerRadius: am5.percent(40)
        })
    );

    const series = chart.series.push(
        am5percent.PieSeries.new(exerciseRoot, {
            valueField: "value",
            categoryField: "category",
            alignLabels: false
        })
    );

    // Slice labels (white)
    series.labels.template.setAll({
        fill: am5.color("#ffffff"),
        fontSize: 14
    });

    // Tick lines (white)
    series.ticks.template.setAll({
        stroke: am5.color("#ffffff")
    });

    // Soft pastel palette
    series.set("colors", am5.ColorSet.new(exerciseRoot, {
        colors: [
            am5.color("#E194A8"),
            am5.color("#EEB0B5"),
            am5.color("#C9A7EB"),
            am5.color("#A5B4FC"),
            am5.color("#8BD3E6"),
            am5.color("#F7C8E0"),
            am5.color("#F9E2AE")
        ],
        reuse: true
    }));

    // Convert totals → chart data
    const exerciseData = Object.entries(exerciseTotals)
        .filter(([_, value]) => value > 0)
        .map(([key, value]) => ({
            category: key,
            value: value
        }));

    series.data.setAll(exerciseData);

    // Legend (must be created BEFORE styling)
    // Legend styling
    const legend = chart.children.push(
        am5.Legend.new(exerciseRoot, {
            centerX: am5.percent(50),
            x: am5.percent(50),
            marginTop: 10,
            marginBottom: 10,
            useDefaultMarker: true
        })
    );

    legend.valueLabels.template.set("forceHidden", true);
    legend.labels.template.set("text", "{category}");

    // NOW apply white text
    legend.labels.template.setAll({
        fill: am5.color("#ffffff"),
        fontSize: 13
    });

    legend.data.setAll(series.dataItems);

    series.appear(1000, 100);
}
    // -----------------------------
    // MOOD SUMMARY
    // -----------------------------
function showMood(viewId, allData) {
    const moodResult = averageMood(allData);

    // Find the summary label for this view
    const suffix = viewId.replace("-view", "");
    const moodLabel = document.getElementById(`mood-summary-${suffix}`);

    if (!moodLabel) {
        console.warn("Mood label element not found for:", viewId);
        return;
    }

    // If no mood logged
    if (moodResult.average === null) {
        moodLabel.innerHTML = `
            <div class="mood-wrapper">
                <span>No mood logged</span>
            </div>
        `;
        return;
    }

    // Map mood label → image filename
    const moodToImage = {
        "Very Happy": "mood_happy.png",
        "Happy": "mood_happy.png",
        "Neutral": "mood_neutral.png",
        "Low": "mood_sad.png",
        "Sad": "mood_sad.png",
        "Stressed": "mood_angry.png"
    };

    const imgFile = moodToImage[moodResult.label] || "mood.png";

    // Update the UI
    moodLabel.innerHTML = `
        <div class="mood-wrapper">
        <h3> Overall Mood </h3>
            <img src="/static/assets/images/${imgFile}" class="mood-icon">
        </div>
    `;
}

function averageMood(allData) {
    let totalMood = 0;
    let count = 0;

    for (let day of allData) {
        const moodSource = day.journal_day?.mood;
        if (!moodSource) continue;

        const moods = Array.isArray(moodSource) ? moodSource : [moodSource];

        console.log("Processing moods for day:", day.journal_day.date, moods);

        moods.forEach(mood => {
            switch (mood.toLowerCase()) {
                case "happy":
                    totalMood += 5;
                    break;
                case "excited":
                    totalMood += 4;
                    break;
                case "neutral":
                    totalMood += 3;
                    break;
                case "sad":
                    totalMood += 1;
                    break;
                case "angry":
                    totalMood += 0;
                    break;
                case "anxious":
                case "stressed":
                    totalMood += -2;
                    break;
            }
        });

        count += moods.length;
    }

    if (count === 0) {
        return {
            average: null,
            label: "No mood logged"
        };
    }

    const avg = totalMood / count;

    let label = "";
    if (avg >= 4.5) label = "Very Happy";
    else if (avg >= 3.5) label = "Happy";
    else if (avg >= 2.5) label = "Neutral";
    else if (avg >= 1.5) label = "Low";
    else if (avg >= 0.5) label = "Sad";
    else label = "Stressed";

    return {
        average: avg,
        label: label
    };
}
    // -----------------------------
    // CALCULATE CALORIES
    // -----------------------------
function calculateTotalCalories(allData) {
    let totalCalories = 0;
    allData.forEach(day => {
        if (Array.isArray(day.food)) {
            day.food.forEach(f => {
                totalCalories += f.calories;
            }
        );
        }
    });
    const caloriesElements = document.querySelectorAll('.summary-value');
    caloriesElements.forEach(elem => {
        elem.textContent = `${totalCalories.toLocaleString()} kcal`;
    });
}

    // -----------------------------
    // Init + toggle handling
    // -----------------------------
    function initFor(viewId) {
        const allData = showView(viewId);
        const transactionTotals = computeTransactionCategories(allData);
        const exerciseTotals = computeExerciseCategories(allData);
        showMood(viewId, allData);
        buildTransactionChart(viewId, transactionTotals);
        buildExerciseChart(viewId, exerciseTotals);
        calculateTotalCalories(allData);
    }

    document.addEventListener("DOMContentLoaded", () => {
        const initial = document.querySelector('input[name="view"]:checked').value;
        initFor(initial);

        document.querySelectorAll('input[name="view"]').forEach(radio => {
            radio.addEventListener("change", () => {
                initFor(radio.value);
            });
        });
    });

});