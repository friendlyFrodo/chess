import pygame
from piece import Piece


def valueTransformerGetBitBoardPosition(row, column):
    return 63 - (row * 8 + column)


class Board:
    def __init__(self):
        whitePawnBitBoard = int("0000000000000000000000000000000000000000000000001111111100000000", 2)
        whiteRookBitBoard = int("0000000000000000000000000000000000000000000000000000000010000001", 2)
        whiteKnightBitBoard = int("0000000000000000000000000000000000000000000000000000000001000010", 2)
        whiteBishopBitBoard = int("0000000000000000000000000000000000000000000000000000000000100100", 2)
        whiteQueenBitBoard = int("0000000000000000000000000000000000000000000000000000000000010000", 2)
        whiteKingBitBoard = int("0000000000000000000000000000000000000000000000000000000000001000", 2)
        blackPawnBitBoard = int("0000000011111111000000000000000000000000000000000000000000000000", 2)
        blackRookBitBoard = int("1000000100000000000000000000000000000000000000000000000000000000", 2)
        blackKnightBitBoard = int("0100001000000000000000000000000000000000000000000000000000000000", 2)
        blackBishopBitBoard = int("0010010000000000000000000000000000000000000000000000000000000000", 2)
        blackQueenBitBoard = int("0001000000000000000000000000000000000000000000000000000000000000", 2)
        blackKingBitBoard = int("0000100000000000000000000000000000000000000000000000000000000000", 2)

        bitBoardsDictionary = {
            "wk": whiteKingBitBoard,
            "wq": whiteQueenBitBoard,
            "wr": whiteRookBitBoard,
            "wn": whiteKnightBitBoard,
            "wb": whiteBishopBitBoard,
            "wp": whitePawnBitBoard,
            "bk": blackKingBitBoard,
            "bq": blackQueenBitBoard,
            "br": blackRookBitBoard,
            "bn": blackKnightBitBoard,
            "bb": blackBishopBitBoard,
            "bp": blackPawnBitBoard
        }
        self.state = bitBoardsDictionary
        self.whiteToMove = True
        self.whiteCastledKingSide = False
        self.whiteCastledQueenSide = False
        self.blackCastledKingSide = False
        self.blackCastledQueenSide = False
        self.piece = None
        self.moveLog = []

    def getState(self):
        return self.state

    def drawBoardState(self, screen):
        for pieceName, bitboard in self.state.items():
            for j in range(64):
                if (bitboard >> j) & int(
                        "000000000000000000000000000000000000000000000000000000000000000000000001") == 1:
                    row = 7 - (j // 8)
                    column = 7 - (j % 8)
                    piece = Piece(name=pieceName, position=j)
                    screen.blit(piece.image, (column * 100, row * 100))

    @staticmethod
    def clear_bit(value, position):
        mask = ~(1 << position)
        return value & mask

    @staticmethod
    def set_bit(value, position):
        mask = 1 << position
        return value | mask

    @staticmethod
    def valueTransformerGetRowCommaColumn(bitboardPosition):
        return bitboardPosition // 8, bitboardPosition % 8

    @staticmethod
    def bitBoardPos2Coords(bitBoardPosition):
        x = (7-bitBoardPosition//8)*100
        y = (7-bitBoardPosition % 8)*100
        return x, y

    @staticmethod
    def coords2bitBoardPos(event):
        x = event.pos[0]
        y = event.pos[1]
        row = y // 100
        column = x // 100
        return valueTransformerGetBitBoardPosition(row, column)

    def pieceOnCoords(self, event):
        bitBoardPosition = self.coords2bitBoardPos(event=event)
        for name, bitBoard in self.state.items():
            if (bitBoard >> bitBoardPosition &
                    int("0000000000000000000000000000000000000000000000000000000000000001") == 1):
                self.piece = Piece(name=name, position=bitBoardPosition)
                return self.piece

    def playMove(self, pieceName, earlierPosition, bitBoardPosition):
        oldstate = self.state.copy()
        for name, bitBoard in self.state.items():
            if pieceName == name:
                bitBoard = self.clear_bit(value=bitBoard, position=earlierPosition)
                bitBoard = self.set_bit(bitBoard, bitBoardPosition)
                self.state[name] = bitBoard
            else:
                bitBoard = self.clear_bit(value=bitBoard, position=bitBoardPosition)
                self.state[name] = bitBoard
        turn = len(self.moveLog) + 1
        self.moveLog.append((turn, self.piece.name, earlierPosition, oldstate, bitBoardPosition, self.state))
        print(self.moveLog)
        self.whiteToMove = not self.whiteToMove

    def chosePieceOnBitBoardPosition(self, bitBoardPosition, pieceName):
        piece = Piece(pieceName, bitBoardPosition)
        self.piece = piece

    def undoLastMove(self):
        self.state = self.moveLog[-1][3]
        self.moveLog.pop()
        self.whiteToMove = not self.whiteToMove

    def dropPiece(self, event):
        bitBoardPosition = self.coords2bitBoardPos(event=event)
        pieceName = self.piece.name
        earlierPosition = self.piece.position
        possibleMoves = self.findPossibleMovesforClickedPiece()
        one = int("0000000000000000000000000000000000000000000000000000000000000001")
        if possibleMoves >> bitBoardPosition & one == one:
            self.playMove(pieceName, earlierPosition, bitBoardPosition)  # playing the move
            breakInnerLoop = False
            # testing if it was illegal because now your king still stands in check
            if self.whiteToMove:
                for pieceName in ["wq", "wk", "wb", "wr", "wn", "wp"]:
                    if breakInnerLoop:
                        break
                    pieceBitBoard = self.state[pieceName]
                    for j in range(64):
                        if pieceBitBoard >> j & one == one:
                            self.chosePieceOnBitBoardPosition(j, pieceName)
                            pieceMoveBitBoard = self.findPossibleMovesforClickedPiece()
                            if pieceMoveBitBoard & self.state["bk"] != 0:
                                self.undoLastMove()  # king in check remove the played move
                                breakInnerLoop = True
                                break
            else:
                for pieceName in ["bq", "bk", "bb", "br", "bn", "bp"]:
                    if breakInnerLoop:
                        break
                    pieceBitBoard = self.state[pieceName]
                    for j in range(64):
                        if pieceBitBoard >> j & one == one:
                            self.chosePieceOnBitBoardPosition(j, pieceName)
                            pieceMoveBitBoard = self.findPossibleMovesforClickedPiece()
                            if pieceMoveBitBoard & self.state["wk"] != 0:
                                breakInnerLoop = True
                                self.undoLastMove()

    def findPossibleMovesforClickedPiece(self):
        if self.piece.name[0] == "w" and not self.whiteToMove or self.piece.name[0] == "b" and self.whiteToMove:
            return 0
        if self.piece.name == "wq" or self.piece.name == "bq":
            return self.findPseudoSlidingMoves(directions=[-9, -8, -7, -1, 1, 7, 8, 9])
        elif self.piece.name == "wr" or self.piece.name == "br":
            return self.findPseudoSlidingMoves(directions=[-8, -1, 1, 8])
        elif self.piece.name == "wb" or self.piece.name == "bb":
            return self.findPseudoSlidingMoves(directions=[-9, -7, 7, 9])
        elif self.piece.name == "wk" or self.piece.name == "bk":
            return self.findPseudoSlidingMoves(directions=[-9, -8, -7, -1, 1, 7, 8, 9])
        elif self.piece.name == "wn" or self.piece.name == "bn":
            return self.findPseudoKnightMoves()
        elif self.piece.name == "wp" or self.piece.name == "bp":
            return self.findPseudoPawnMoves()
        else:
            return int("0000000000000000000000000000000000000000000000000000000000000000")

    def drawPossibleMoves(self, screen, bitboard):
        if bitboard is None:
            return
        one = int("0000000000000000000000000000000000000000000000000000000000000001")
        green = (0, 255, 0)
        dot_radius = 5
        for j in range(64):
            if bitboard >> j & one == 1:
                x, y = self.bitBoardPos2Coords(j)
                pygame.draw.circle(screen, green, (y + 50, x + 50), dot_radius)

    # TODO: check for checks in next pseudomoves of opponent | en-passant | rochade | promotion

    def findPseudoPawnMoves(self):
        enemyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        friendlyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        pseudoMovesBitBoard = int("0000000000000000000000000000000000000000000000000000000000000000")
        one = int("0000000000000000000000000000000000000000000000000000000000000001")
        for name, bitBoard in self.state.items():
            if name[0] == self.piece.name[0]:
                friendlyPiecePositions = friendlyPiecePositions | bitBoard
            elif name[0] != self.piece.name[0]:
                enemyPiecePositions = enemyPiecePositions | bitBoard
        possibleMoves = []
        if (self.piece.position // 8 == 1
                and self.piece.name == "wp"
                and enemyPiecePositions >> self.piece.position+8 & one != one
                and enemyPiecePositions >> self.piece.position+16 & one != one
                and friendlyPiecePositions >> self.piece.position+8 & one != one
                and friendlyPiecePositions >> self.piece.position+16 & one != one):
            possibleMoves.append(16)
        if (self.piece.name == "wp"
                and enemyPiecePositions >> self.piece.position+8 & one != one
                and friendlyPiecePositions >> self.piece.position+8 & one != one):
            possibleMoves.append(8)
        if self.piece.name == "wp" and enemyPiecePositions >> self.piece.position+9 & one == one:
            possibleMoves.append(9)
        if self.piece.name == "wp" and enemyPiecePositions >> self.piece.position+7 & one == one:
            possibleMoves.append(7)

        if (self.piece.position // 8 == 6
                and self.piece.name == "bp"
                and enemyPiecePositions >> self.piece.position-8 & one != one
                and enemyPiecePositions >> self.piece.position-16 & one != one
                and friendlyPiecePositions >> self.piece.position-8 & one != one
                and friendlyPiecePositions >> self.piece.position-16 & one != one):
            possibleMoves.append(-16)
        if (self.piece.name == "bp" and enemyPiecePositions >> self.piece.position-8 & one != one
                and friendlyPiecePositions >> self.piece.position-8 & one != one):
            possibleMoves.append(-8)
        if self.piece.name == "bp" and enemyPiecePositions >> self.piece.position-9 & one == one:
            possibleMoves.append(-9)
        if self.piece.name == "bp" and enemyPiecePositions >> self.piece.position-7 & one == one:
            possibleMoves.append(-7)

        for move in possibleMoves:
            if self.piece.position + move > 63 or self.piece.position + move < 0:
                continue
            if friendlyPiecePositions >> (self.piece.position + move) & one == 1:
                continue
            elif enemyPiecePositions >> (self.piece.position + move) & one == 1:
                pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + move)
            else:
                pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + move)
        return pseudoMovesBitBoard

    def findPseudoKnightMoves(self):
        enemyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        friendlyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        pseudoMovesBitBoard = int("0000000000000000000000000000000000000000000000000000000000000000")
        one = int("0000000000000000000000000000000000000000000000000000000000000001")
        for name, bitBoard in self.state.items():
            if name[0] == self.piece.name[0]:
                friendlyPiecePositions = friendlyPiecePositions | bitBoard
            elif name[0] != self.piece.name[0]:
                enemyPiecePositions = enemyPiecePositions | bitBoard
        possibleMoves = [17, 15, 10, 6, -6, -10, -15, -17]
        for move in possibleMoves:
            if self.piece.position + move > 63 or self.piece.position + move < 0:
                continue
            if friendlyPiecePositions >> (self.piece.position + move) & one == 1:
                continue
            elif enemyPiecePositions >> (self.piece.position + move) & one == 1:
                pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + move)
            else:
                pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + move)
        return pseudoMovesBitBoard

    def findPseudoSlidingMoves(self, directions):
        enemyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        friendlyPiecePositions = int("0000000000000000000000000000000000000000000000000000000000000000")
        pseudoMovesBitBoard = int("0000000000000000000000000000000000000000000000000000000000000000")
        one = int("0000000000000000000000000000000000000000000000000000000000000001")
        for name, bitBoard in self.state.items():
            if name[0] == self.piece.name[0]:
                friendlyPiecePositions = friendlyPiecePositions | bitBoard
            elif name[0] != self.piece.name[0]:
                enemyPiecePositions = enemyPiecePositions | bitBoard
        for direction in directions:
            i = 1
            while True:
                zeilenspruenge = (self.piece.position+i*direction)//8-self.piece.position//8
                print(f"zeilensprünge: {zeilenspruenge} für feld: {self.piece.position+i*direction}")
                if self.piece.position + i * direction > 63 or self.piece.position + i * direction < 0:
                    break
                if friendlyPiecePositions >> (self.piece.position + i*direction) & one == 1:
                    break
                if (direction == 1 or direction == -1) and zeilenspruenge != 0:
                    break
                if direction > 6 and zeilenspruenge != i or direction < -6 and zeilenspruenge != -i:
                    break
                elif enemyPiecePositions >> (self.piece.position + i*direction) & one == 1:
                    pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + i*direction)
                    break
                else:
                    pseudoMovesBitBoard = self.set_bit(pseudoMovesBitBoard, self.piece.position + i * direction)
                    if self.piece.name == "wk" or self.piece.name == "bk":
                        break
                    i += 1
        return pseudoMovesBitBoard
