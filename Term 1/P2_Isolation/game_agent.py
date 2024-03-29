"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # set scores for winning/losing
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    # get number of blank spaces left
    spaces = len(game.get_blank_spaces())
    # get number of remaining moves
    remaining = len(game.get_legal_moves(player))
    # define new score: keep as many remaining spaces of available open
    score = remaining / float(spaces)

    return float(score)


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # set scores for winning/losing
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    # get player pos
    pos = game.get_player_location(player)
    # get opponent position
    opos = game.get_player_location(game.get_opponent(player))
    # set generic score
    score = 0
    # define new score: stay as far away from opponent
    if pos and opos:
        score = abs(opos[0]-pos[0])+abs(opos[1]-pos[1])
    return float(score)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    # set scores for winning/losing
    if game.is_loser(player):
        return float("-inf")
    if game.is_winner(player):
        return float("inf")

    # get player pos
    pos = game.get_player_location(player)
    # get opponent position
    opos = game.get_player_location(game.get_opponent(player))
    # set generic score
    score = 0
    # define new score: stay as close to opponent as possible
    if pos and opos:
        score = abs(opos[0] - pos[0]) + abs(opos[1] - pos[1])
    return 1/float(score)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        # get available legal moves from board
        legal_moves = game.get_legal_moves()
        # replace with (-1,-1) if there are no legal moves
        if not legal_moves:
            legal_moves = (-1, -1)

        # PSEUDOCODE REF: https://www.youtube.com/watch?v=J1GoI5WHBto

        # create a generic best move
        best_move = (-1,-1)
        # define the value for best move
        best_val = float('-inf')
        # loop through each move
        # choose the move that has the max value after starting the recursion through mmin
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the minimum value for the current child nodes (recursively)
            val = self.mmin(f_game, depth-1)
            # get the maximum of the best val and the found val
            # replace best val and best move
            if val > best_val:
                best_val = val
                best_move = move

        return best_move

    def mmax(self,game,depth):
        '''
        Find the max value for all possible moves for a player in a game
        i.e. all of the child nodes of a given state of the game
        :param game: the board object
        :param depth: the current depth of the plies of the game tree
        :return: the highest value
        '''
        # copy timer check into helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get available legal moves from board
        legal_moves = game.get_legal_moves()
        # if terminal node or no legal moves
        if depth == 0 or not legal_moves:
            # return the score of the current node
            return self.score(game, self)

        # set the best value to negative infinity
        best_val = float('-inf')

        # loop through all the child nodes
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the minimum value for the subsequent child nodes (recursively)
            val = self.mmin(f_game,depth-1)
            # get the maximum of the best val and the found val
            best_val = max(val, best_val)

        # return the best value
        return best_val

    def mmin(self, game, depth):
        '''
        Find the min value for all possible moves for a player in a game
        i.e. all of the child nodes of a given state of the game
        :param game: the board object
        :param depth: the current depth of the plies of the game tree
        :return: the lowest value
        '''
        # copy timer check into helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get available legal moves from board
        legal_moves = game.get_legal_moves()
        # if terminal node or no legal moves
        if depth == 0 or not legal_moves:
            # return the score of the current node
            return self.score(game, self)

        # set the best value to positive infinity
        best_val = float('inf')

        # loop through all the child nodes
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the maximum value for the subsequent child nodes (recursively)
            val = self.mmax(f_game, depth-1)
            # get the min of the best val and the found val
            best_val = min(val, best_val)

        # return the best value
        return best_val


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.

            # create a counter for depth starting at next pli aka 1
            pli = 1
            while True:
                # run the ab function
                best_move = self.alphabeta(game, pli)
                # increment the depth
                pli += 1
                # get best value
                best_val =self.score(game.forecast_move(best_move),self)
                # if val reaches infinity, break the loop
                if best_val == float('inf') or best_val == float('-inf'):
                    break
            #return self.alphabeta(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed
            #return best_move

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # TODO: finish this function!

        # get available legal moves from board
        legal_moves = game.get_legal_moves()

        # create a generic best move
        best_move = (-1, -1)
        # define a generic starting value for best value
        best_val = float('-inf')

        # replace with (-1,-1) if there are no legal moves
        if not legal_moves:
            return best_move

        # loop through each move
        # choose the move that has the max value after starting the recursion through mmin
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the minimum value for the current child nodes (recursively)
            val = self.abmin(f_game, depth-1, alpha, beta)
            # update alpha for pruning
            alpha = max(alpha, val)
            # get the maximum of the best val and the found val
            # replace best val and best move
            if val >= best_val:
                best_val = val
                best_move = move

        return best_move

    def abmax(self, game, depth, alpha, beta):
        '''
        Find the max value for all possible moves for a player in a game
        i.e. all of the child nodes of a given state of the game
        :param game: the board object
        :param depth: the current depth of the plies of the game tree
        :param alpha: the ab function alpha value
        :param beta: the ab function beta value
        :return: tuple - the highest value, the best move
        '''
        # copy timer check into helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get available legal moves from board
        legal_moves = game.get_legal_moves()
        # if no legal moves
        if not legal_moves:
            # return the current state
            return game.utility(self)

        # if terminal node
        if depth == 0:
            # return the score of the terminal node
            return self.score(game, self)

        # set the best value to negative infinity
        best_val = float('-inf')
        # create a generic best move
        best_move = (-1, -1)

        # loop through all the child nodes
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the minimum value for the subsequent child nodes (recursively)
            val = self.abmin(f_game, depth - 1, alpha, beta)
            # get the maximum of the best val and the found val
            if val > best_val:
                best_val = val
            #best_val = max(val, best_val)
            # if best_val is greater than or equal to beta
            if best_val >= beta:
                return best_val
            alpha = max(alpha, best_val)
        # return the best value
        return best_val

    def abmin(self, game, depth, alpha, beta):
        '''
        Find the min value for all possible moves for a player in a game
        i.e. all of the child nodes of a given state of the game
        :param game: the board object
        :param depth: the current depth of the plies of the game tree
        :param alpha: the ab function alpha value
        :param beta: the ab function beta value
        :return: tuple - the lowest value, the best move
        '''
        # copy timer check into helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get available legal moves from board
        legal_moves = game.get_legal_moves()
        # if no legal moves
        if not legal_moves:
            # return the current state
            return game.utility(self)

        # if terminal node
        if depth == 0:
            # return the score of the terminal node
            return self.score(game, self)

        # set the best value to positive infinity
        best_val = float('inf')
        # create a generic best move
        best_move = (-1, -1)

        # loop through all the child nodes
        for move in legal_moves:
            # get the forecasted board for the child node
            f_game = game.forecast_move(move)
            # get the maximum value for the subsequent child nodes (recursively)
            val = self.abmax(f_game, depth - 1, alpha, beta)
            # get the min of the best val and the found val
            if val < best_val:
                best_val = val
            #best_val = min(val, best_val)
            # if best_val is less than or equal to alpha
            if best_val <= alpha:
                # return the best value and best move
                return best_val
            beta = min(beta, best_val)
        # return the best value and best move
        return best_val
