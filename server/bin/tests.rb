#!/usr/bin/env ruby
#
# Yeah let's face it, shell scripting is for suckers
require 'json'

def req(url, data=nil)
    data_arg = !data.nil? ? "-d " + "'" + data + "'" : ""
    results = `curl -s #{data_arg} '#{url}'`
    return JSON.parse(results)
end

player_nicks = ['arnold', 'betty', 'chuck']
player_urls_map = {}
game_id = nil

player_nicks.each_with_index do |nick, i|
    if i == 0
        result = req('http://localhost:8000/game/new', "num_players=3&nick=#{nick}")
    else
        result = req("http://localhost:8000/game/#{game_id}/join", "nick=#{nick}")
    end
    # Will keep overwriting, that's fine
    game_id = result['game']['id']
    player_urls_map[result['player']['number']] = result['game_url']
end

puts "PLAYERS:", player_urls_map

round_start = true
round_number = 1
player_dice_map = {}

begin
    if round_start
        puts "*" * 70
        puts "ROUND ##{round_number}"
        round_start = false
    end

    # Everybody fetches their dice roll
    for player_num, url in player_urls_map
        result = req(url)
        player_dice_map[result['player']['id']] = result['player']['dice']
        # Will keep overwriting, that's fine
        player_turn = result['game']['player_turn']
        last_gamble = result['game']['last_gamble']
    end

    if last_gamble.nil? || last_gamble == ""
        upped_dice = '1,1'
    else
        upped_dice = last_gamble.split(',').map { |v| v.to_i }
        upped_dice[rand(1)] += 1
        upped_dice = upped_dice.join(',')
    end

    decisions = {
        0.05 => "exact",
        0.2  => "bullshit",
        1.0  => upped_dice,
    }
    r = rand()
    decisions.reject! { |prob, option| prob < r }
    _, gamble = decisions.first

    url = player_urls_map[player_turn]
    result = req("#{url}/do_turn", "gamble=#{gamble}")

    puts "    -> #{player_nicks[player_turn-1]} gambles on '#{gamble}'"

    if result['error']
        puts "    !! #{result['error']}"
    else
        rn = result['game']['round'].to_i
        if round_number < rn
            round_number = rn
            round_start = true
        end
    end
end while result['error'] || result['game']['player_won'].nil?
