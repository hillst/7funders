# Seven Wonders Simulator

Simple python based prototype for 7 wonders. The aim is AI driven development. Should be easy to code AI for this game and should be easy to play across a network. Ultimately we should rely onjavascript/html5 for a front end and rebrand the game as something else. 

## Software Design goals

- Design a game interface that is simple for a MCTS agent or any MDP type agent.
- Design a game where *game design itself* is treated as an MDP.
    - Data driven game design. Can computationallty identify strategies
- Support non-standard cards and an AI-driven approach to game design
- Ultimately if this game should be different than 7 wonders:
    - More balanced
    - More interesting

## Game design goals

Here is my researchless totally emprically mandates for good game design:

1) Anyone can win (newcomes and pros)
    - Easy to address with randomness, think mario kart
2) More skilled players should win more often
    - Complex strategies should support this
3) Minimal downtime between turns (how often are players waiting)
4) Small enough gaps to allow for drinks/snacks
5) Should be simple to understand (much like 7wonders basegame)
6) Balanced gameplay -- the mean win % or rank should be uniform across strategies. Strategies should have different variances
    - High variance strategies should be easy to identify ("timmy")
    - Low variance strategies should be hard to identify ("spike")
    - Should have some round-about strategies that work well consistently ("johnny")
