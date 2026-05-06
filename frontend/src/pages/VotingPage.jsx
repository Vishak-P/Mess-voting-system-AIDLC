/**
 * Voting page - shows weekly menu grouped by date.
 * Students can vote for one dish per meal.
 */
import React, { useEffect, useState, useCallback } from "react";
import api from "../utils/api";
import { getErrorMessage, groupMenusByDate, sortMeals, formatDate } from "../utils/helpers";
import MenuCard from "../components/MenuCard";
import VoteModal from "../components/VoteModal";
import { CardLoader } from "../components/Loader";
import toast from "react-hot-toast";
import { FiCalendar, FiChevronLeft, FiChevronRight } from "react-icons/fi";
import { format, startOfWeek, endOfWeek, addWeeks } from "date-fns";

const VotingPage = () => {
  const [menus, setMenus] = useState([]);
  const [myVotes, setMyVotes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [voteLoading, setVoteLoading] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState(null);
  const [selectedExistingOptionId, setSelectedExistingOptionId] = useState(null);
  const [weekOffset, setWeekOffset] = useState(0);

  // Compute week range
  const weekStart = startOfWeek(addWeeks(new Date(), weekOffset), { weekStartsOn: 1 });
  const weekEnd = endOfWeek(addWeeks(new Date(), weekOffset), { weekStartsOn: 1 });
  const weekLabel = `${format(weekStart, "MMM d")} – ${format(weekEnd, "MMM d, yyyy")}`;

  const fetchData = useCallback(async () => {
    setLoading(true);
    try {
      const weekStr = format(weekStart, "yyyy-'W'ww");
      const [menusRes, votesRes] = await Promise.all([
        api.get(`/menus?week=${weekStr}`),
        api.get("/my-votes"),
      ]);
      setMenus(menusRes.data.menus);
      setMyVotes(votesRes.data.votes);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [weekOffset]); // eslint-disable-line react-hooks/exhaustive-deps

  useEffect(() => { fetchData(); }, [fetchData]);

  const handleVoteSubmit = async (menuId, optionId) => {
    setVoteLoading(true);
    try {
      const { data } = await api.post("/vote", { menu_id: menuId, option_id: optionId });
      const isChange = data.message?.includes("updated");
      toast.success(isChange ? "Vote updated! 🔄" : "Vote cast! 🎉");
      setSelectedMenu(null);
      setSelectedExistingOptionId(null);
      fetchData();
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setVoteLoading(false);
    }
  };

  // Called by MenuCard: onVoteClick(menu, existingOptionId | null)
  const handleVoteClick = (menu, existingOptionId) => {
    setSelectedMenu(menu);
    setSelectedExistingOptionId(existingOptionId ?? null);
  };

  const grouped = groupMenusByDate(menus);
  const sortedDates = Object.keys(grouped).sort();

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <FiCalendar className="text-blue-600" />
            Weekly Menu
          </h1>
          <p className="text-gray-500 text-sm mt-1">{weekLabel}</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={() => setWeekOffset((w) => w - 1)}
            className="btn-secondary p-2"
            aria-label="Previous week"
          >
            <FiChevronLeft />
          </button>
          <button
            onClick={() => setWeekOffset(0)}
            className="btn-secondary text-sm px-3 py-2"
          >
            This Week
          </button>
          <button
            onClick={() => setWeekOffset((w) => w + 1)}
            className="btn-secondary p-2"
            aria-label="Next week"
          >
            <FiChevronRight />
          </button>
        </div>
      </div>

      {loading ? (
        <CardLoader count={4} />
      ) : sortedDates.length === 0 ? (
        <div className="card text-center py-12">
          <p className="text-4xl mb-3">📭</p>
          <p className="text-gray-600 font-medium">No menus for this week</p>
          <p className="text-gray-400 text-sm mt-1">Check back later or try another week</p>
        </div>
      ) : (
        <div className="space-y-8">
          {sortedDates.map((date) => (
            <div key={date}>
              <h2 className="text-base font-semibold text-gray-700 mb-3 flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-500 inline-block" />
                {formatDate(date, "EEEE, MMMM d")}
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {sortMeals(grouped[date]).map((menu) => {
                  const userVote = myVotes.find((v) => v.menu_id === menu.id);
                  return (
                    <MenuCard
                      key={menu.id}
                      menu={menu}
                      userVotedOptionId={userVote?.option_id}
                      onVoteClick={handleVoteClick}
                      showVoteButton
                    />
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Vote modal */}
      {selectedMenu && (
        <VoteModal
          menu={selectedMenu}
          existingVoteOptionId={selectedExistingOptionId}
          onClose={() => { setSelectedMenu(null); setSelectedExistingOptionId(null); }}
          onSubmit={handleVoteSubmit}
          loading={voteLoading}
        />
      )}
    </div>
  );
};

export default VotingPage;
