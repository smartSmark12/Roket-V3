baseBiomeWeights = [
                    [950, 400, 200, 100, 300],
                    [200, 980, 500, 150, 250],
                    [50, 400, 980, 300, 350],
                    [50, 50, 600, 970, 300],
                    [400, 200, 250, 150, 990]
]

# format [chanceToStay, [[:otherBiomeWeights], [:otherBiomeWeights], ...]] (?)
## NOPE -> format: [0 %, 1 %, 2 %, 3 %, 4 %, ...]

# 0 grass, 1 forest, 2 mountains, 3 desert, 4 ocean

# grass (95%) -> forest 40%, ocean 25%, mountains 20%, desert 10%
# forest (98%) -> mountains 50%, grass 20%, ocean 25%, desert 15%
# mountains (98%) -> forest 40%, ocean 35%, desert 20%, grass 5% 
# desert (97%) -> mountains 60%, ocean 30%, grass 5%, forest 5%
# ocean (99%) -> grass 40%, mountains 25%, forest 20%, desert 15%

grassyBiomeWeights = [
                    [960, 450, 200, 100, 250],
                    [300, 980, 400, 150, 250],
                    [50, 450, 980, 200, 300],
                    [50, 50, 600, 970, 300],
                    [400, 200, 250, 150, 990]
]

mountains_plateaus_lakesBiomeWeights = [
                    [950, 400, 200, 100, 300],
                    [200, 980, 500, 150, 250],
                    [50, 400, 980, 300, 350],
                    [50, 50, 600, 970, 300],
                    [400, 200, 250, 150, 990]
]
