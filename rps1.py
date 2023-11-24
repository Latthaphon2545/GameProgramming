# The code is implementing a game of Rock Paper Scissors with an undeterministic AI opponent. It
# allows the player to play against the AI in a series of rounds. The AI opponent uses a stochastic
# approach based on Markov chains to determine its next move. The code keeps track of the number of
# wins for the player, wins for the AI, and draws. It also records the player's command and updates
# the probability of certain sequences of moves in the playerProb dictionary.
# The code is implementing a game of Rock Paper Scissors with an undeterministic AI opponent.
# Game programming Rock Paper Scissors with Undeterministic AI
import random

numPlayerWon = 0
numAiWon = 0
numDraw = 0
actions = ["r", "p", "s"]
round = 0
playerSeq = []
playerProb = [{
    "rrr": 0, "rrp": 0, "rrs": 0,
    "rpr": 0, "rpp": 0, "rps": 0,
    "rsr": 0, "rsp": 0, "rss": 0,
    "prr": 0, "prp": 0, "prs": 0,
    "ppr": 0, "ppp": 0, "pps": 0,
    "psr": 0, "psp": 0, "pss": 0,
    "srr": 0, "srp": 0, "srs": 0,
    "spr": 0, "spp": 0, "sps": 0,
    "ssr": 0, "ssp": 0, "sss": 0,
}]

predicAction = actions[random.randint(0, 2)]
goodAnswer = {'r': 'p', 'p': 's', 's': 'r'}

while True:
    # simple random Ai
    # aiCommand = actions[random.randint(0,2)]
    # Stochastic Ai https://en.wikipedia.org/wiki/Markov_chain

    # Get Ai command
    if len(playerSeq) <= 1:
        predicAction = actions[random.randint(0, 2)]
    else:
        propR = playerProb[0][playerSeq[-2]+playerSeq[-1]+'r']
        propP = playerProb[0][playerSeq[-2]+playerSeq[-1]+'p']
        propS = playerProb[0][playerSeq[-2]+playerSeq[-1]+'s']
        if (propR >= propP and propR >= propS):
            predicAction = 'r'
        elif (propP >= propR and propP >= propS):
            predicAction = 'p'
        elif (propS >= propR and propS >= propP):
            predicAction = 's'

    if random.randint(0, 1):
        aiCommand = goodAnswer[predicAction]
    else:
        aiCommand = predicAction # make it draw


    # Record player command
    print("Round " + str(round+1))

    # Get player command
    playerCommand = input("Rock(r) : Paper(p) : Shortgun(s)  \nP=> ").lower()
    if playerCommand == 'q':
        print(playerSeq)
        print(playerProb)
        quit()
    elif playerCommand not in actions:
        continue

    round += 1
    # Record player command
    playerSeq.append(playerCommand)
    if len(playerSeq) >= 3:
        playerProb[0][playerSeq[-3]+playerSeq[-2]+playerSeq[-1]] += 1

    # process base on game rules
    print("P=>"+playerCommand+" vs "+aiCommand+"<=Ai")
    if playerCommand == aiCommand:
        print("    Draw")
        numDraw += 1
    elif (playerCommand == "r" and aiCommand == "s") or (playerCommand == "p" and aiCommand == "r") or (playerCommand == "s" and aiCommand == "p"):
        print("  You Win")
        numPlayerWon += 1
    else:
        print("  You Lost")
        numAiWon += 1
    print("  P: " + str(numPlayerWon)+" Ai: " +
          str(numAiWon) + " Draw: "+str(numDraw) + "\n")
