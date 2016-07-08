import random

from GameObject import GameObject
from enemy import Dumb
from enemy import Follower
from enemy import Avoider
from enemy import Brick
from Point import Point

MAX_BRICKS = 1

ENEMIES = [
    # level 1
    [
        Dumb.Dumb,
        Follower.Follower,
    ],
    # level 2
    [
        Dumb.Dumb,
        Follower.Follower,
        Avoider.Avoider,
    ],
    # level 3
    [
        Dumb.Dumb,
        Follower.Follower,
        Avoider.Avoider,
        Brick.Brick,
    ],
]

TICKS_PER_SEC = 60
INTERVALS = [
    2.0,
    1.5,
    1.3,
]


class Spawner(GameObject):
    def __init__(self, scene, level=0):
        super().__init__(scene)
        self.timer = 0
        self.level = level
        self.interval = INTERVALS[level]

    def update(self):
        self.level = self._resolve_level()
        self.interval = INTERVALS[self.level]*TICKS_PER_SEC
        if self.timer <= 0:
            for i in range(self._resolve_count()):
                self._spawn()
            self.timer = self.interval
        else:
            self.timer -= 1

    def _spawn(self):
        while True:
            x = random.randrange(0, self.scene.size[0])
            y = random.randrange(0, self.scene.size[1])
            if (Point(x, y) - self.scene.player.position).length() > 100:
                break

        enemy_set = ENEMIES[self.level]
        enemy_type = random.choice(enemy_set)

        # avoid LAGGGG
        if enemy_type == Brick.Brick:
            bricks = 0
            for obj in self.scene.objects:
                if isinstance(obj, Brick.Brick):
                    bricks += 1
            if bricks >= MAX_BRICKS:
                rest = enemy_set[:]
                rest.remove(Brick.Brick)
                enemy_type = random.choice(rest)

        enemy_obj = enemy_type(self.scene, x, y)
        self.scene.add_object(enemy_obj)

    def _resolve_count(self):
        score = self.scene.player.score
        count = int(self.scene.player.score/1500)
        return min(count, 2) + 1

    def _resolve_level(self):
        score = self.scene.player.score
        return min(2, int(score/2000))
