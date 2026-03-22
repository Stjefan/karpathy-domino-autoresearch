#include <bits/stdc++.h>
using namespace std;

struct Cell { int x, y; };
struct Piece { vector<Cell> cells; };

static vector<Cell> normalize(vector<Cell> pts) {
    int minx = INT_MAX, miny = INT_MAX;
    for (auto &c : pts) { minx = min(minx, c.x); miny = min(miny, c.y); }
    for (auto &c : pts) { c.x -= minx; c.y -= miny; }
    sort(pts.begin(), pts.end(), [](const Cell& a, const Cell& b){ return a.x == b.x ? a.y < b.y : a.x < b.x; });
    return pts;
}

static vector<Cell> transform_piece_raw(const vector<Cell>& cells, int r, int f) {
    vector<Cell> out;
    out.reserve(cells.size());
    for (auto c : cells) {
        int x = c.x, y = c.y;
        if (f) x = -x;
        int nx, ny;
        switch (r & 3) {
            case 0: nx = x; ny = y; break;
            case 1: nx = y; ny = -x; break;
            case 2: nx = -x; ny = -y; break;
            default: nx = -y; ny = x; break;
        }
        out.push_back({nx, ny});
    }
    return out;
}

struct Choice {
    int idx, r, f, w, h, box_area, cells;
    int minx, miny;
    vector<Cell> shape;
};

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    if (!(cin >> n)) return 0;
    vector<Piece> pieces(n);
    long long total_cells = 0;
    for (int i = 0; i < n; ++i) {
        int k; cin >> k;
        pieces[i].cells.resize(k);
        total_cells += k;
        for (int j = 0; j < k; ++j) cin >> pieces[i].cells[j].x >> pieces[i].cells[j].y;
    }

    vector<Choice> choices;
    choices.reserve(n);
    int min_width = 1;

    for (int i = 0; i < n; ++i) {
        Choice best{};
        best.idx = i;
        best.box_area = INT_MAX;
        best.w = best.h = INT_MAX;
        best.cells = (int)pieces[i].cells.size();

        set<vector<pair<int,int>>> seen;
        for (int f = 0; f <= 1; ++f) {
            for (int r = 0; r < 4; ++r) {
                auto raw = transform_piece_raw(pieces[i].cells, r, f);
                int minx = INT_MAX, miny = INT_MAX, maxx = INT_MIN, maxy = INT_MIN;
                for (auto &c : raw) {
                    minx = min(minx, c.x);
                    miny = min(miny, c.y);
                    maxx = max(maxx, c.x);
                    maxy = max(maxy, c.y);
                }
                auto t = normalize(raw);
                vector<pair<int,int>> sig;
                for (auto &c : t) sig.push_back({c.x, c.y});
                if (!seen.insert(sig).second) continue;

                int w = maxx - minx + 1;
                int h = maxy - miny + 1;
                int area = w * h;
                if (area < best.box_area ||
                    (area == best.box_area && max(w, h) < max(best.w, best.h)) ||
                    (area == best.box_area && max(w, h) == max(best.w, best.h) && w > best.w)) {
                    best = {i, r, f, w, h, area, (int)t.size(), minx, miny, t};
                }
            }
        }
        min_width = max(min_width, best.w);
        choices.push_back(best);
    }

    sort(choices.begin(), choices.end(), [](const Choice& a, const Choice& b) {
        if (a.box_area != b.box_area) return a.box_area > b.box_area;
        if (a.h != b.h) return a.h > b.h;
        if (a.w != b.w) return a.w > b.w;
        return a.cells > b.cells;
    });

    int start_width = max<int>(min_width, sqrt((double)max<long long>(1, total_cells)));
    long long best_area = (1LL << 62);
    int best_w = start_width, best_h = (int)total_cells;
    vector<array<int,4>> best_ans(n);

    for (int W = start_width; W <= start_width + 32; ++W) {
        vector<array<int,4>> ans(n);
        vector<vector<unsigned char>> occ;
        vector<int> col_height(W, 0);

        auto ensure_rows = [&](int need_rows) {
            while ((int)occ.size() < need_rows) occ.emplace_back(W, 0);
        };

        auto can_place = [&](const Choice& c, int px, int py) {
            if (px < 0 || px + c.w > W || py < 0) return false;
            ensure_rows(py + c.h);
            for (const auto& cell : c.shape) {
                if (occ[py + cell.y][px + cell.x]) return false;
            }
            return true;
        };

        auto place = [&](const Choice& c, int px, int py) {
            ensure_rows(py + c.h);
            for (const auto& cell : c.shape) {
                occ[py + cell.y][px + cell.x] = 1;
                col_height[px + cell.x] = max(col_height[px + cell.x], py + cell.y + 1);
            }
        };

        for (const auto& c : choices) {
            int best_x = -1, best_y = INT_MAX;
            for (int x = 0; x + c.w <= W; ++x) {
                int y = 0;
                for (const auto& cell : c.shape) {
                    y = max(y, col_height[x + cell.x] - cell.y);
                }
                while (!can_place(c, x, y)) ++y;
                if (y < best_y || (y == best_y && x < best_x)) {
                    best_x = x;
                    best_y = y;
                }
            }
            place(c, best_x, best_y);
            ans[c.idx] = {best_x - c.minx, best_y - c.miny, c.r, c.f};
        }

        int H = 0;
        for (int h : col_height) H = max(H, h);
        long long area = 1LL * W * H;
        if (area < best_area || (area == best_area && H < best_h) || (area == best_area && H == best_h && W < best_w)) {
            best_area = area;
            best_w = W;
            best_h = H;
            best_ans = ans;
        }
    }

    cout << best_w << ' ' << best_h << '\n';
    for (int i = 0; i < n; ++i) {
        cout << best_ans[i][0] << ' ' << best_ans[i][1] << ' ' << best_ans[i][2] << ' ' << best_ans[i][3] << '\n';
    }
    return 0;
}
